from __future__ import annotations

import sys

import numpy as np
from scipy.spatial.transform import Rotation  # type: ignore
from cartesian_axis import Axis, CoordinateHandedness
from units import AngleUnit

from ...order import IntrinsicRotationOrder, ExtrinsicRotationOrder
from ..protocol import HandedRotationMatrixProtocol

if sys.version_info >= (3, 11):
    from typing import TYPE_CHECKING, Self, cast
else:
    from typing import TYPE_CHECKING, cast

    from typing_extensions import Self

if TYPE_CHECKING:
    from ...euler import EulerAngles


class RotationMatrixConvertMixin:
    """Conversions to other representations (handedness tag, Euler angles)."""

    @staticmethod
    def _axis_reflection_matrix(axis: Axis) -> np.ndarray:
        match axis:
            case Axis.X:
                return np.diag([-1.0, 1.0, 1.0])
            case Axis.Y:
                return np.diag([1.0, -1.0, 1.0])
            case Axis.Z:
                return np.diag([1.0, 1.0, -1.0])

    def to_opposite_handedness(self, *, flip_axis: Axis = Axis.Z) -> Self:
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
        Self
            Same orthogonal SO(3) map with flipped coordinate_handedness metadata.
        """
        h = cast(HandedRotationMatrixProtocol, self)
        D = self._axis_reflection_matrix(flip_axis)
        new_value = D @ h.value @ D
        match h.coordinate_handedness:
            case CoordinateHandedness.RIGHT:
                new_handedness = CoordinateHandedness.LEFT
            case CoordinateHandedness.LEFT:
                new_handedness = CoordinateHandedness.RIGHT
        return cast(
            Self,
            type(self)(
                value=new_value,  # type: ignore[call-arg]
                coordinate_handedness=new_handedness,  # type: ignore[call-arg]
            ),
        )

    def to_euler_angles(
        self,
        order: IntrinsicRotationOrder | ExtrinsicRotationOrder,
        unit: AngleUnit,
    ) -> EulerAngles:
        """
        Euler angles via SciPy (internally right-handed).

        angle progression follows SciPy for this matrix as SO(3); it does not reinterpret signs for
        a left-handed coordinate_handedness tag on its own.
        """
        from ...euler import EulerAngles

        h = cast(HandedRotationMatrixProtocol, self)
        r = Rotation.from_matrix(h.value)
        raw_euler_angles = r.as_euler(
            order.value,
            degrees=unit.is_degree,
        )
        return EulerAngles(
            value=raw_euler_angles,
            order=order,
            unit=unit,
        )
