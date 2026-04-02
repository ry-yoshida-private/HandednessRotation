from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property

from cartesian_axis import CoordinateHandedness
from scipy.spatial.transform import Rotation # type: ignore

from rotation import Quaternion as Q

from ..matrix import RotationMatrix


@dataclass(frozen=True)
class Quaternion(Q):
    """
    Container class for quaternion representation of rotation with coordinate handedness.

    Inherits validation and format handling from Quaternion; adds a handedness tag
    used when building a HandednessRotationMatrix from this quaternion.

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

    @cached_property
    def rotation_matrix(self) -> RotationMatrix:
        """
        Convert quaternion to rotation matrix with handedness metadata.

        Uses scipy.spatial.transform.Rotation; the resulting 3x3 matrix must still
        satisfy HandednessRotationMatrix determinant rules for coordinate_handedness.

        Returns
        -------
        HandednessRotationMatrix:
            The rotation matrix representation.
        """
        scipy_rotation = Rotation.from_quat(
            self.value,
            scalar_first=self.is_scalar_first,
        )
        return RotationMatrix(
            value=scipy_rotation.as_matrix(),
            coordinate_handedness=self.coordinate_handedness,
        )
