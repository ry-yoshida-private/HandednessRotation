from __future__ import annotations

import numpy as np
from scipy.spatial.transform import Rotation # type: ignore
from dataclasses import dataclass
from typing import TYPE_CHECKING

from cartesian_axis import Axis, CoordinateHandedness
from rotation import RotationMatrix as R
from units import AngleUnit

from .order import IntrinsicRotationOrder, ExtrinsicRotationOrder

if TYPE_CHECKING:
    from .euler import EulerAngles


@dataclass(frozen=True)
class RotationMatrix(R):
    """
    Container class for rotation matrix representation with coordinate handedness.

    Extends RotationMatrix (pure SO(3)-style validation on the base type) with a
    CoordinateHandedness tag for which frame convention this rotation is expressed in.

    Rotations are proper orthogonal matrices in SO(3) (determinant +1) for both RIGHT and LEFT.
    The tag records which handedness convention this matrix is meant for; it does not replace an
    axis-flip when exchanging data with another pipeline. Composing with @ requires the same tag.

    scipy.spatial.transform.Rotation (see to_euler_angles) assumes a right-handed frame internally,
    so Euler angles from that path describe this matrix as an SO(3) map in the usual mathematical
    sense; interpreting angle direction under a left-handed convention still needs your own rules.

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
        If the rotation matrix does not have determinant +1 (not a proper rotation).
    """

    coordinate_handedness: CoordinateHandedness

    def __post_init__(self):
        if not self.is_determinant_correct:
            determinant = np.linalg.det(self.value)
            raise ValueError(f"Rotation matrix must have determinant +1 (not a proper rotation), got determinant {determinant}")

    @property
    def is_determinant_correct(self) -> bool:
        """
        True if this matrix is a proper rotation (orthogonal with determinant +1).

        Returns
        -------
        bool:
            True if determinant is +1 within tolerance, False otherwise.
        """
        return np.isclose(np.linalg.det(self.value), 1.0, atol=1e-6)

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

    @staticmethod
    def _axis_reflection_matrix(axis: Axis) -> np.ndarray:
        match axis:
            case Axis.X:
                return np.diag([-1.0, 1.0, 1.0])
            case Axis.Y:
                return np.diag([1.0, -1.0, 1.0])
            case Axis.Z:
                return np.diag([1.0, 1.0, -1.0])

    def to_opposite_handedness(self, *, flip_axis: Axis = Axis.Z) -> RotationMatrix:
        """
        Represent the same proper rotation under the opposite handedness tag using one axis flip.

        Computes R' = D @ R @ D where D reflects flip_axis (orthogonal, det(D) = -1, D @ D = I).
        Then det(R') = +1 still holds. Which axis to flip is a convention (often Z in graphics);
        match it to the change-of-basis between your left-handed and right-handed setups.

        Parameters
        ----------
        flip_axis : Axis
            Coordinate axis reflected by D.

        Returns
        -------
        RotationMatrix
            Same orthogonal SO(3) map with flipped coordinate_handedness metadata.
        """
        D = self._axis_reflection_matrix(flip_axis)
        new_value = D @ self.value @ D
        match self.coordinate_handedness:
            case CoordinateHandedness.RIGHT:
                new_handedness = CoordinateHandedness.LEFT
            case CoordinateHandedness.LEFT:
                new_handedness = CoordinateHandedness.RIGHT
        return RotationMatrix(value=new_value, coordinate_handedness=new_handedness)

    def __matmul__(
        self,
        other: R,
    ) -> RotationMatrix:
        """
        Multiply two handedness rotation matrices.

        Parameters
        ----------
        other : R
            Right-hand operand; must be this package's RotationMatrix with matching handedness.

        Returns
        -------
        RotationMatrix:
            The matrix product, with the same coordinate_handedness as self.

        Raises
        ------
        TypeError:
            If other is not a RotationMatrix.
        ValueError:
            If other is a handedness RotationMatrix but coordinate_handedness differs from self.
        """
        match other:
            case RotationMatrix(coordinate_handedness=h) if h == self.coordinate_handedness:
                return RotationMatrix(
                    value=self.value @ other.value,
                    coordinate_handedness=self.coordinate_handedness,
                )
            case RotationMatrix():
                raise ValueError(
                    "Cannot compose rotations with different coordinate_handedness tags."
                )
            case R():
                raise TypeError(
                    "RotationMatrix @ other requires another handedness RotationMatrix; use plain RotationMatrix @ RotationMatrix from the base package if handedness is not needed."
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
        RotationMatrix:
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

        The orthogonal factor Q is reflected if needed so det(Q) is +1 (proper rotation).

        Parameters
        ----------
        value: np.ndarray
            The approximate rotation matrix.
        coordinate_handedness: CoordinateHandedness
            The coordinate handedness.

        Returns
        -------
        RotationMatrix:
            The closest valid rotation matrix from the QR factor.
        """
        Q, _ = np.linalg.qr(value) # Q, R
        if np.linalg.det(Q) < 0:
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

        The reconstructed orthogonal matrix is reflected if needed so its determinant is +1.

        Parameters
        ----------
        value: np.ndarray
            The approximate rotation matrix.
        coordinate_handedness: CoordinateHandedness
            The coordinate handedness.

        Returns
        -------
        RotationMatrix:
            The valid rotation matrix from the SVD-based orthogonalization.
        """
        u, _, vh = np.linalg.svd(value) # u, s, vh
        rotation_matrix = u @ vh

        if np.linalg.det(rotation_matrix) < 0:
            u[:, -1] *= -1
            rotation_matrix = u @ vh

        return cls(
            value=rotation_matrix,
            coordinate_handedness=coordinate_handedness,
        )

    def to_euler_angles(
        self, 
        order: IntrinsicRotationOrder | ExtrinsicRotationOrder,
        unit: AngleUnit
        ) -> EulerAngles:
        """
        Euler angles via SciPy (internally right-handed).

        angle progression follows SciPy for this matrix as SO(3); it does not reinterpret signs for
        a left-handed coordinate_handedness tag on its own.
        """
        from .euler import EulerAngles
        r = Rotation.from_matrix(self.value)
        raw_euler_angles = r.as_euler(
            order.value, 
            degrees=unit.is_degree
            )
        return EulerAngles(
            value=raw_euler_angles,
            order=order,
            unit=unit
            )

