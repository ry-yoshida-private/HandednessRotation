from __future__ import annotations

import numpy as np
from dataclasses import dataclass
from typing import Callable

from cartesian_axis import Axis, CoordinateHandedness
from rotation import RotationMatrix as R


@dataclass(frozen=True)
class RotationMatrix(R):
    """
    Container class for rotation matrix representation with coordinate handedness.

    Extends RotationMatrix (pure SO(3)-style validation on the base type) with a
    CoordinateHandedness tag. Determinant checks follow the former rotation copy
    convention: right-handed frames expect determinant +1, left-handed -1.

    Attributes
    ----------
    value: np.ndarray
        The rotation matrix as a 3x3 matrix.
    coordinate_handedness: CoordinateHandedness
        The coordinate handedness (CoordinateHandedness.RIGHT or CoordinateHandedness.LEFT).

    Raises
    ------
    ValueError:
        If the rotation matrix is not a 3x3 matrix.
        If the rotation matrix is not orthogonal.
        If the rotation matrix does not have the correct determinant for the handedness.
    """

    coordinate_handedness: CoordinateHandedness

    @property
    def is_determinant_correct(self) -> bool:
        """
        Check if the rotation matrix has the correct determinant for this handedness.

        Returns
        -------
        bool:
            True if the determinant matches the handedness rule, False otherwise.
        """
        match self.coordinate_handedness:
            case CoordinateHandedness.RIGHT:
                return np.isclose(np.linalg.det(self.value), 1.0, atol=1e-6)
            case CoordinateHandedness.LEFT:
                return np.isclose(np.linalg.det(self.value), -1.0, atol=1e-6)

    def extract_axis_rotation(
        self,
        axis: Axis,
    ) -> np.ndarray:
        """
        Extract the column of the rotation matrix for the given Cartesian axis.

        Parameters
        ----------
        axis: Axis
            The axis to extract (X, Y, or Z).

        Returns
        -------
        np.ndarray:
            The corresponding column of the rotation matrix, shape (3,).
        """
        match axis:
            case Axis.X:
                return self.value[:, 0]
            case Axis.Y:
                return self.value[:, 1]
            case Axis.Z:
                return self.value[:, 2]

    def __matmul__(
        self,
        other: R,
    ) -> R:
        """
        Multiply two handedness rotation matrices.

        Parameters
        ----------
        other: R
            Right-hand operand; must be another HandednessRotationMatrix.

        Returns
        -------
        R:
            The matrix product, with the same coordinate_handedness as self.

        Raises
        ------
        TypeError:
            If other is not a RotationMatrix.
        ValueError:
            If the coordinate handednesses are not the same.
        """
        if not isinstance(other, RotationMatrix):
            raise TypeError(
                "HandednessRotationMatrix @ other requires another HandednessRotationMatrix; use from_rotation_matrix or plain RotationMatrix @ RotationMatrix otherwise."
            )
        if other.coordinate_handedness != self.coordinate_handedness:
            raise ValueError(
                "Invalid rotation matrix: coordinate systems must be the same"
            )
        return RotationMatrix(
            value=self.value @ other.value,
            coordinate_handedness=self.coordinate_handedness,
        )

    @classmethod
    def unit_matrix(
        cls,
        coordinate_handedness: CoordinateHandedness = CoordinateHandedness.RIGHT,
    ) -> RotationMatrix:
        """
        Create the identity rotation matrix with a given handedness.

        Parameters
        ----------
        coordinate_handedness: CoordinateHandedness
            The coordinate handedness.

        Returns
        -------
        HandednessRotationMatrix:
            The 3x3 identity matrix tagged with coordinate_handedness.
        """
        return cls(
            value=np.eye(3),
            coordinate_handedness=coordinate_handedness,
        )

    @classmethod
    def from_approximate_matrix_by_qr(
        cls,
        value: np.ndarray,
        coordinate_handedness: CoordinateHandedness = CoordinateHandedness.RIGHT,
    ) -> RotationMatrix:
        """
        Build a valid rotation matrix from an approximate 3x3 matrix using QR decomposition.

        The orthogonal factor Q is adjusted so its determinant matches coordinate_handedness.

        Parameters
        ----------
        value: np.ndarray
            The approximate rotation matrix.
        coordinate_handedness: CoordinateHandedness
            The coordinate handedness.

        Returns
        -------
        HandednessRotationMatrix:
            The closest valid rotation matrix from the QR factor.
        """
        Q, _ = np.linalg.qr(value) # Q, R
        det = np.linalg.det(Q)

        criterion: Callable[[float], bool]
        match coordinate_handedness:
            case CoordinateHandedness.RIGHT:
                criterion = lambda d: d < 0
            case CoordinateHandedness.LEFT:
                criterion = lambda d: d > 0
        if criterion(det):
            Q[:, -1] *= -1
        return cls(
            value=Q, 
            coordinate_handedness=coordinate_handedness
            )

    @classmethod
    def from_approximate_matrix_with_SVD(
        cls,
        value: np.ndarray,
        coordinate_handedness: CoordinateHandedness = CoordinateHandedness.RIGHT,
    ) -> RotationMatrix:
        """
        Build a valid rotation matrix from an approximate 3x3 matrix using SVD.

        The reconstructed orthogonal matrix is adjusted so its determinant matches
        coordinate_handedness.

        Parameters
        ----------
        value: np.ndarray
            The approximate rotation matrix.
        coordinate_handedness: CoordinateHandedness
            The coordinate handedness.

        Returns
        -------
        HandednessRotationMatrix:
            The valid rotation matrix from the SVD-based orthogonalization.
        """
        u, _, vh = np.linalg.svd(value) # u, s, vh
        rotation_matrix = u @ vh

        criterion: Callable[[np.ndarray], bool]
        match coordinate_handedness:
            case CoordinateHandedness.RIGHT:
                criterion = lambda rm: np.linalg.det(rm) < 0
            case CoordinateHandedness.LEFT:
                criterion = lambda rm: np.linalg.det(rm) > 0
        if criterion(rotation_matrix):
            u[:, -1] *= -1
            rotation_matrix = u @ vh

        return cls(
            value=rotation_matrix,
            coordinate_handedness=coordinate_handedness,
        )
