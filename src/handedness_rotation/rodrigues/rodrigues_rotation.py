from __future__ import annotations
import numpy as np
from dataclasses import dataclass
from functools import cached_property


from cartesian_axis import CoordinateHandedness
from rotation import RodriguesRotationParameter as RRP, SkewSymmetricMatrix

from ..matrix import RotationMatrix


@dataclass(frozen=True)
class RodriguesRotationParameter(RRP):
    """
    Container class for Rodrigues rotation parameter with coordinate handedness.

    Attributes
    ----------
    value: np.ndarray
        The Rodrigues rotation parameter (length-3 vector).
    coordinate_handedness: CoordinateHandedness
        The coordinate handedness carried through to rotation_matrix.
    """

    coordinate_handedness: CoordinateHandedness

    @cached_property
    def rotation_matrix(self) -> RotationMatrix:
        """
        Convert Rodrigues rotation parameter to rotation matrix.

        Returns
        -------
        HandednessRotationMatrix:
            The rotation matrix tagged with coordinate_handedness.
        """
        theta = np.linalg.norm(self.value)

        if theta < 1e-6:
            return RotationMatrix(
                value=np.eye(3),
                coordinate_handedness=self.coordinate_handedness,
            )

        # Normalized axis for Rodrigues formula; base class has no handedness field.
        normalized_rodrigues = RRP(value=self.value / theta)

        K = SkewSymmetricMatrix.from_k_parameter(
            k_x=normalized_rodrigues.x,
            k_y=normalized_rodrigues.y,
            k_z=normalized_rodrigues.z,
        )

        I = np.eye(3)  # Identity matrix
        skew_term = np.sin(theta) * K.value
        symmetric_term = (1 - np.cos(theta)) * K.squared
        R = I + skew_term + symmetric_term

        return RotationMatrix(
            value=R,
            coordinate_handedness=self.coordinate_handedness,
        )
