from __future__ import annotations

import sys

import numpy as np
from cartesian_axis import Axis, CoordinateHandedness
from rotation import RotationMatrix as R

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


class RotationMatrixFactoryMixin(R):
    """
    Single anchor to rotation.RotationMatrix: carries value validation and lets
    classmethods call cls(..., value=..., coordinate_handedness=...) with sane typing.

    Combine only with plain mixins ahead of this one in the final class bases so R
    appears once in the MRO.
    """

    @classmethod
    def unit_matrix(
        cls,
        coordinate_handedness: CoordinateHandedness = CoordinateHandedness.RIGHT,
    ) -> Self:
        """
        Create the identity rotation matrix with a given handedness.

        Parameters
        ----------
        coordinate_handedness: CoordinateHandedness
            The coordinate handedness.

        Returns
        -------
        Self:
            The 3x3 identity matrix tagged with coordinate_handedness.
        """
        return cls(
            value=np.eye(3),
            coordinate_handedness=coordinate_handedness,  # type: ignore[call-arg]
        )

    @classmethod
    def from_approximate_matrix_by_qr(
        cls,
        value: np.ndarray,
        coordinate_handedness: CoordinateHandedness = CoordinateHandedness.RIGHT,
    ) -> Self:
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
        Self:
            The closest valid rotation matrix from the QR factor.
        """
        Q, _ = np.linalg.qr(value)  # Q, R
        if np.linalg.det(Q) < 0:
            Q[:, -1] *= -1
        return cls(
            value=Q,
            coordinate_handedness=coordinate_handedness,  # type: ignore[call-arg]
        )

    @classmethod
    def from_approximate_matrix_with_SVD(
        cls,
        value: np.ndarray,
        coordinate_handedness: CoordinateHandedness = CoordinateHandedness.RIGHT,
    ) -> Self:
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
        Self:
            The valid rotation matrix from the SVD-based orthogonalization.
        """
        u, _, vh = np.linalg.svd(value)  # u, s, vh
        rotation_matrix = u @ vh

        if np.linalg.det(rotation_matrix) < 0:
            u[:, -1] *= -1
            rotation_matrix = u @ vh

        return cls(
            value=rotation_matrix,
            coordinate_handedness=coordinate_handedness,  # type: ignore[call-arg]
        )

    @classmethod
    def from_axis_angle(
        cls,
        axis: Axis,
        angle: float,
        coordinate_handedness: CoordinateHandedness = CoordinateHandedness.RIGHT,
    ) -> Self:
        """
        Elementary rotation: a right-handed angle in radians about the given axis.

        Parameters
        ----------
        axis: Axis
            Cartesian axis (X, Y, or Z).
        angle: float
            Rotation angle in radians (positive follows the right-hand rule about the rotation axis).
        coordinate_handedness: CoordinateHandedness
            Tag for the resulting matrix.

        Returns
        -------
        Self:
            The 3x3 rotation matrix for that single-axis rotation.
        """
        c = float(np.cos(angle))
        s = float(np.sin(angle))

        match axis:
            case Axis.X:
                value = np.array(
                    [
                        [1.0, 0.0, 0.0],
                        [0.0, c, -s],
                        [0.0, s, c],
                    ],
                    dtype=np.float64,
                )
            case Axis.Y:
                value = np.array(
                    [
                        [c, 0.0, s],
                        [0.0, 1.0, 0.0],
                        [-s, 0.0, c],
                    ],
                    dtype=np.float64,
                )
            case Axis.Z:
                value = np.array(
                    [
                        [c, -s, 0.0],
                        [s, c, 0.0],
                        [0.0, 0.0, 1.0],
                    ],
                    dtype=np.float64,
                )

        return cls(
            value=value,
            coordinate_handedness=coordinate_handedness,  # type: ignore[call-arg]
        )
