from enum import Enum
from typing import Generator
from cartesian_axis import Axis

class IntrinsicRotationOrder(Enum):
    """
    Intrinsic rotation order for scipy.spatial.transform.Rotation.

    Attributes
    ----------
    XYZ: XYZ rotation order.
    XZY: XZY rotation order.
    YXZ: YXZ rotation order.
    YZX: YZX rotation order.
    ZXY: ZXY rotation order.
    ZYX: ZYX rotation order.
    """

    XYZ = "XYZ"
    XZY = "XZY"
    YXZ = "YXZ"
    YZX = "YZX"
    ZXY = "ZXY"
    ZYX = "ZYX"

    @property
    def as_upper(self) -> str:
        """
        Return the rotation order as uppercase.
        
        Returns
        -------
        str:
            The rotation order as uppercase.
        """
        return str(self.value).upper()
    
    @property
    def as_lower(self) -> str:
        """
        Return the rotation order as lowercase.
        
        Returns
        -------
        str:
            The rotation order as lowercase.
        """
        return str(self.value).lower()

    def __iter__(self) -> Generator[Axis, None, None]:
        """
        Iterate axes in the rotation order.
        
        Returns
        -------
        Generator[Axis, None, None]:
            The generator of the rotation order.
        """
        for axis in self.value:
            yield Axis(axis)
