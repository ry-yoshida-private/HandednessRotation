import numpy as np

from ..order import ExtrinsicRotationOrder, IntrinsicRotationOrder
from ..axis import RotationAxis
from cartesian_axis import AxisOrientation, Axis


class EulerIndexMapper:
    """
    Mapper for Euler angles(roll, pitch, yaw) to their indices(0, 1, 2) in the rotation order.
    
    Attributes
    ----------
    euler_index_mapper: dict[RotationAxis, int]
        The mapper for Euler angles to their indices in the rotation order.
    """
    def __init__(
        self,
        rotation_order: ExtrinsicRotationOrder | IntrinsicRotationOrder,
        axis_orientation: AxisOrientation
        ) -> None:
        """
        Initialize the Euler index mapper.
        
        Parameters
        ----------
        rotation_order: ExtrinsicRotationOrder | IntrinsicRotationOrder
            The rotation order of the Euler angles.
        forward_axis: Axis
            The forward axis.
        right_axis: Axis
            The right axis.
        up_axis: Axis
            The up axis.
        """
        self.euler_index_mapper = EulerIndexMapper.get_euler_index_mapper(
            rotation_order=rotation_order,
            axis_orientation=axis_orientation
            )
    
    @staticmethod
    def get_euler_index_mapper(
        rotation_order: ExtrinsicRotationOrder | IntrinsicRotationOrder, 
        axis_orientation: AxisOrientation
        ) -> dict[RotationAxis, int]:
        """
        Obtain a mapping that associates each Euler angle (roll, pitch, yaw)
        with the corresponding axis in the Cartesian coordinate system and
        its index in the given rotation order.

        Parameters
        ----------
        rotation_order : ExtrinsicRotationOrder | IntrinsicRotationOrder
            The rotation order of the Euler angles.
        forward_axis : Axis
            The axis used to represent the forward direction.
        right_axis : Axis
            The axis used to represent the right direction.
        up_axis : Axis
            The axis used to represent the upward direction.

        Returns
        -------
        dict[RotationAxis, int]
            A mapping from Euler angles (roll, pitch, yaw) to their indices
            according to the specified rotation order.
        """

        axis_map : dict[Axis, RotationAxis] = {
            axis_orientation.forward: RotationAxis.ROLL,
            axis_orientation.right: RotationAxis.PITCH,
            axis_orientation.up: RotationAxis.YAW
        }
        return {axis_map[rot_axis]: i for i, rot_axis in enumerate(rotation_order)}


    def __call__(
        self, 
        euler_angles: np.ndarray
        ) -> np.ndarray:
        """
        Map Euler angles to their indices in the rotation order.
        
        Parameters
        ----------
        euler_angles: np.ndarray
            The Euler angles to map.

        Returns
        -------
        np.ndarray:
            The Euler angles in the rotation order(roll, pitch, yaw).
        """
        return np.array([
            euler_angles[self.euler_index_mapper[RotationAxis.ROLL]], 
            euler_angles[self.euler_index_mapper[RotationAxis.PITCH]], 
            euler_angles[self.euler_index_mapper[RotationAxis.YAW]]
            ]
            )