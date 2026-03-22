from enum import Enum


class RotationAxis(Enum):
    """
    Semantic rotation axes (roll, pitch, yaw).

    Attributes
    ----------
    ROLL: str
        Roll axis.
    PITCH: str
        Pitch axis.
    YAW: str
        Yaw axis.
    """

    ROLL = "roll"
    PITCH = "pitch"
    YAW = "yaw"
