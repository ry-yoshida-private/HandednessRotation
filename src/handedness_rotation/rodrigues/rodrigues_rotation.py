from __future__ import annotations
import numpy as np
from dataclasses import dataclass
from functools import cached_property


from cartesian_axis import CoordinateHandedness
from rotation import RodriguesRotationParameter, SkewSymmetricMatrix

from ..matrix import HandednessRotationMatrix


@dataclass(frozen=True)
class HandednessRodriguesRotationParameter(RodriguesRotationParameter):
    """
    Container class for Rodrigues rotation parameter with coordinate handedness.

    Attributes
    ----------
    value: np.ndarray
        The Rodrigues rotation parameter (length-3 vector).
    coordinate_handedness: CoordinateHandedness
        The coordinate handedness carried through to ``rotation_matrix``.
    """

    coordinate_handedness: CoordinateHandedness

    @cached_property
    def rotation_matrix(self) -> HandednessRotationMatrix:
        """
        Convert Rodrigues rotation parameter to rotation matrix.

        Returns
        -------
        HandednessRotationMatrix:
            The rotation matrix tagged with ``coordinate_handedness``.
        """
        theta = np.linalg.norm(self.value)

        if theta < 1e-6:
            return HandednessRotationMatrix(
                value=np.eye(3),
                coordinate_handedness=self.coordinate_handedness,
            )

        # Normalized axis for Rodrigues formula; base class has no handedness field.
        normalized_rodrigues = RodriguesRotationParameter(value=self.value / theta)

        K = SkewSymmetricMatrix.from_k_parameter(
            k_x=normalized_rodrigues.x,
            k_y=normalized_rodrigues.y,
            k_z=normalized_rodrigues.z,
        )

        I = np.eye(3)  # Identity matrix
        skew_term = np.sin(theta) * K.value
        symmetric_term = (1 - np.cos(theta)) * K.squared
        R = I + skew_term + symmetric_term

        return HandednessRotationMatrix(
            value=R,
            coordinate_handedness=self.coordinate_handedness,
        )
