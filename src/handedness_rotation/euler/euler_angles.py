from __future__ import annotations
import numpy as np
from dataclasses import dataclass

from units import AngleUnit, Angle
from ..order import IntrinsicRotationOrder, ExtrinsicRotationOrder

@dataclass
class EulerAngles:
    """
    Container for a length-3 Euler angle triple and its rotation convention.

    Attributes:
    ----------
    value : np.ndarray
        Shape (3,). value[i] is the angle about the i-th axis named in order
        (same layout as scipy.spatial.transform.Rotation.as_euler).
    order : IntrinsicRotationOrder | ExtrinsicRotationOrder
        Axis sequence for the angles in value.
    unit : AngleUnit
        Angular unit of value.

    Raises
    ------
    ValueError:
        If value does not have shape (3,).

    Notes
    -----
    roll, pitch, and yaw properties read value[0], value[1], and value[2]. Those names match
    body roll/pitch/yaw only when value is stored or interpreted that way (see EulerIndexMapper).
    """
    value: np.ndarray
    order: IntrinsicRotationOrder | ExtrinsicRotationOrder
    unit: AngleUnit

    def __post_init__(self):
        if self.value.shape != (3,):
            raise ValueError(f"Euler angles must have shape (3,), got shape {self.value.shape}")

    @property
    def is_degrees(self) -> bool:
        """
        Return True if the Euler angles are in degrees.
        
        Returns
        -------
        bool:
            True if the Euler angles are in degrees, False otherwise.
        """
        return self.unit == AngleUnit.DEGREE

    @property
    def roll(self) -> Angle:
        """
        Return value[0] as an Angle (roll only when that component is roll).

        Returns
        -------
        Angle:
            First component of value.
        """
        return Angle(
            value=self.value[0], 
            unit=self.unit
            )

    @property
    def pitch(self) -> Angle:
        """
        Return value[1] as an Angle (pitch only when that component is pitch).

        Returns
        -------
        Angle:
            Second component of value.
        """
        return Angle(
            value=self.value[1], 
            unit=self.unit
            )

    @property
    def yaw(self) -> Angle:
        """
        Return value[2] as an Angle (yaw only when that component is yaw).

        Returns
        -------
        Angle:
            Third component of value.
        """
        return Angle(
            value=self.value[2], 
            unit=self.unit
            )

    def __str__(self) -> str:
        return f"EulerAngles(value={self.value}, \
        \norder={self.order}, \
        \nunit={self.unit})"
