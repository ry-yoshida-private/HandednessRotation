from __future__ import annotations

from dataclasses import dataclass

from cartesian_axis import CoordinateHandedness
from rotation import RodriguesRotationParameter as RRP


@dataclass(frozen=True)
class RodriguesRotationParameter(RRP):
    """
    Container class for Rodrigues rotation parameter with coordinate handedness.

    Attributes
    ----------
    value: np.ndarray
        The Rodrigues rotation parameter (length-3 vector).
    coordinate_handedness: CoordinateHandedness
        Convention tag for this parameter. ``rotation_matrix`` is inherited from
        the base class and returns a plain ``float64`` array (same SO(3) map).
    """

    coordinate_handedness: CoordinateHandedness
