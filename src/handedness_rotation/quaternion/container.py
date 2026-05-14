from __future__ import annotations

from dataclasses import dataclass

from cartesian_axis import CoordinateHandedness
from rotation import Quaternion as Q


@dataclass(frozen=True)
class Quaternion(Q):
    """
    Container class for quaternion representation of rotation with coordinate handedness.

    Inherits validation, format handling, and ``rotation_matrix`` (plain ``float64``
    array) from ``rotation.Quaternion``. ``coordinate_handedness`` is metadata only.

    Parameters
    ----------
    value: np.ndarray
        Quaternion values as a 4-element array.
    format: QuaternionFormat
        The format of the quaternion (WXYZ or XYZW).
    coordinate_handedness: CoordinateHandedness
        The coordinate handedness (e.g. CoordinateHandedness.RIGHT).
    """

    coordinate_handedness: CoordinateHandedness
