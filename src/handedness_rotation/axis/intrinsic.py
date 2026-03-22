from enum import Enum


class IntrinsicAxis3D(Enum):
    """
    Intrinsic axis in 3D.

    Enum values use uppercase letters so they can be passed directly to
    ``scipy.spatial.transform.Rotation`` Euler conventions.

    Attributes
    ----------
    X: str
        X-axis (intrinsic).
    Y: str
        Y-axis (intrinsic).
    Z: str
        Z-axis (intrinsic).
    """

    X = "X"
    Y = "Y"
    Z = "Z"
