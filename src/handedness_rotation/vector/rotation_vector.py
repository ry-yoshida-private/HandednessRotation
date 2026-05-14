from __future__ import annotations

from dataclasses import dataclass

from cartesian_axis import CoordinateHandedness
from rotation import RotationVector as RotationVectorBase

from .mixin import RotationVectorFactoryMixin


@dataclass(frozen=True)
class RotationVector(
    RotationVectorFactoryMixin,
    RotationVectorBase,
):
    """
    Rotation vector (axis-angle) tagged with coordinate handedness.

    Direction is the rotation axis and magnitude is the angle in radians, as in
    ``rotation.RotationVector``. ``coordinate_handedness`` records which frame
    convention this object is for; it does not alter ``rotation_matrix`` or other
    numeric maps inherited from the base class.

    Attributes
    ----------
    value : np.ndarray
        Rotation vector with shape (3,).
    coordinate_handedness : CoordinateHandedness
        Convention tag (e.g. ``CoordinateHandedness.RIGHT`` or ``LEFT``).

    Raises
    ------
    ValueError:
        If ``value`` does not have shape (3,).
    """

    coordinate_handedness: CoordinateHandedness
