from __future__ import annotations
import numpy as np
from dataclasses import dataclass

from units import AngleUnit, Angle
from ..order import IntrinsicRotationOrder, ExtrinsicRotationOrder

@dataclass
class EulerAngles:
    """
    Container class for Euler angles (roll, pitch, yaw) representation of rotation.

    Attributes:
    ----------
    value: np.ndarray
        The Euler angles as a 3x1 vector. Order is: roll, pitch, yaw.
    rotation_order: IntrinsicRotationOrder | ExtrinsicRotationOrder
        The order of the Euler angles.
    unit: AngleUnit
        The unit of the Euler angles.

    Raises
    ------
    ValueError:
        If the Euler angles are not a 3x1 vector.
    """
    value: np.ndarray
    rotation_order: IntrinsicRotationOrder | ExtrinsicRotationOrder
    unit: AngleUnit

    def __post_init__(self):
        if self.value.shape != (3,):
            raise ValueError(f"Euler angles must be a 3x1 vector, got shape {self.value.shape}")

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
        Return the roll angle.
        
        Returns
        -------
        Angle:
            The roll angle.
        """
        return Angle(
            value=self.value[0], 
            unit=self.unit
            )

    @property
    def pitch(self) -> Angle:
        """
        Return the pitch angle.
        
        Returns
        -------
        Angle:
            The pitch angle.
        """
        return Angle(
            value=self.value[1], 
            unit=self.unit
            )

    @property
    def yaw(self) -> Angle:
        """
        Return the yaw angle.
        
        Returns
        -------
        Angle:
            The yaw angle.
        """
        return Angle(
            value=self.value[2], 
            unit=self.unit
            )

    def __str__(self) -> str:
        return f"EulerAngles(value={self.value}, \
        \nrotation_order={self.rotation_order}, \
        \nunit={self.unit})"
