from enum import Enum


class ExtrinsicAxis3D(Enum):
    """
    Extrinsic axis in 3D.

    Enum values use lowercase letters so they can be passed directly to
    ``scipy.spatial.transform.Rotation`` Euler conventions.

    Attributes
    ----------
    X: str
        X-axis (extrinsic).
    Y: str
        Y-axis (extrinsic).
    Z: str
        Z-axis (extrinsic).
    """

    X = "x"
    Y = "y"
    Z = "z"
