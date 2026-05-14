from __future__ import annotations

from typing import TypeVar

import numpy as np
import numpy.typing as npt
from cartesian_axis import Axis, CoordinateHandedness

from ..protocol import HandedRotationMatrixProtocol, handed_rotation_matrix_ctor

_R = TypeVar("_R", bound=HandedRotationMatrixProtocol)


class RotationMatrixFactoryMixin:
    """
    Factory classmethods for handedness-tagged rotation matrices.

    Keep this mixin **plain** (do not subclass ``rotation.RotationMatrix``): the
    upstream package already defines a ``RotationMatrixFactoryMixin`` on its
    container; inheriting that type makes overrides clash with static analysis.
    Combine with ``rotation.RotationMatrix`` (or a subclass) in the final class
    bases so ``value`` validation and axis helpers remain available.
    """

    @classmethod
    def unit_matrix(
        cls: type[_R],
        coordinate_handedness: CoordinateHandedness = CoordinateHandedness.RIGHT,
    ) -> _R:
        """
        Create the identity rotation matrix with a given handedness.

        Parameters
        ----------
        coordinate_handedness: CoordinateHandedness
            The coordinate handedness.

        Returns
        -------
        _R:
            The 3x3 identity matrix tagged with coordinate_handedness.
        """
        return handed_rotation_matrix_ctor(cls)(
            value=np.eye(3, dtype=np.float64),
            coordinate_handedness=coordinate_handedness,
        )

    @classmethod
    def from_approximate_matrix_by_qr(
        cls: type[_R],
        value: npt.ArrayLike,
        coordinate_handedness: CoordinateHandedness = CoordinateHandedness.RIGHT,
    ) -> _R:
        """
        Build a valid rotation matrix from an approximate 3x3 matrix using QR decomposition.

        The orthogonal factor Q is reflected if needed so det(Q) is +1 (proper rotation).

        Parameters
        ----------
        value: array_like
            The approximate rotation matrix.
        coordinate_handedness: CoordinateHandedness
            The coordinate handedness.

        Returns
        -------
        _R:
            The closest valid rotation matrix from the QR factor.
        """
        arr = np.asarray(value, dtype=np.float64)
        q, _ = np.linalg.qr(arr)
        if np.linalg.det(q) < 0:
            q = q.copy()
            q[:, -1] *= -1
        return handed_rotation_matrix_ctor(cls)(
            value=q,
            coordinate_handedness=coordinate_handedness,
        )

    @classmethod
    def from_approximate_matrix_with_SVD(
        cls: type[_R],
        value: npt.ArrayLike,
        coordinate_handedness: CoordinateHandedness = CoordinateHandedness.RIGHT,
    ) -> _R:
        """
        Build a valid rotation matrix from an approximate 3x3 matrix using SVD.

        The reconstructed orthogonal matrix is reflected if needed so its determinant is +1.

        Parameters
        ----------
        value: array_like
            The approximate rotation matrix.
        coordinate_handedness: CoordinateHandedness
            The coordinate handedness.

        Returns
        -------
        _R:
            The valid rotation matrix from the SVD-based orthogonalization.
        """
        arr = np.asarray(value, dtype=np.float64)
        u, _, vh = np.linalg.svd(arr)
        rotation_matrix: np.ndarray = u @ vh

        if np.linalg.det(rotation_matrix) < 0:
            u = u.copy()
            u[:, -1] *= -1
            rotation_matrix = u @ vh

        return handed_rotation_matrix_ctor(cls)(
            value=rotation_matrix,
            coordinate_handedness=coordinate_handedness,
        )

    @classmethod
    def from_axis_angle(
        cls: type[_R],
        axis: Axis,
        angle: float,
        coordinate_handedness: CoordinateHandedness = CoordinateHandedness.RIGHT,
    ) -> _R:
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
        _R:
            The 3x3 rotation matrix for that single-axis rotation.
        """
        c = float(np.cos(angle))
        s = float(np.sin(angle))

        match axis:
            case Axis.X:
                mat = np.array(
                    [
                        [1.0, 0.0, 0.0],
                        [0.0, c, -s],
                        [0.0, s, c],
                    ],
                    dtype=np.float64,
                )
            case Axis.Y:
                mat = np.array(
                    [
                        [c, 0.0, s],
                        [0.0, 1.0, 0.0],
                        [-s, 0.0, c],
                    ],
                    dtype=np.float64,
                )
            case Axis.Z:
                mat = np.array(
                    [
                        [c, -s, 0.0],
                        [s, c, 0.0],
                        [0.0, 0.0, 1.0],
                    ],
                    dtype=np.float64,
                )

        return handed_rotation_matrix_ctor(cls)(
            value=mat,
            coordinate_handedness=coordinate_handedness,
        )
