import numpy as np

from ..order import ExtrinsicRotationOrder, IntrinsicRotationOrder
from ..axis import RotationAxis
from cartesian_axis import AxisOrientation, Axis


class EulerIndexMapper:
    """
    Maps semantic Euler axes (roll, pitch, yaw) to indices in a given rotation order, and reorders
    angle vectors from that order to canonical [roll, pitch, yaw].

    Attributes
    ----------
    euler_index_mapper : dict[RotationAxis, int]
        For each RotationAxis, the index at which that angle appears in rotation_order.
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
        rotation_order : ExtrinsicRotationOrder | IntrinsicRotationOrder
            Sequence of rotation axes; euler_angles[i] corresponds to rotation_order[i].
        axis_orientation : AxisOrientation
            Which Cartesian axes are forward, right, and up; these are mapped to roll, pitch, yaw.
        """
        self.euler_index_mapper: dict[RotationAxis, int] = EulerIndexMapper.get_euler_index_mapper(
            rotation_order=rotation_order,
            axis_orientation=axis_orientation
            )
    
    @staticmethod
    def get_euler_index_mapper(
        rotation_order: ExtrinsicRotationOrder | IntrinsicRotationOrder, 
        axis_orientation: AxisOrientation
        ) -> dict[RotationAxis, int]:
        """
        Build a mapping from each semantic angle (roll, pitch, yaw) to its index in
        rotation_order, using axis_orientation to tie Cartesian axes to roll/pitch/yaw.

        Parameters
        ----------
        rotation_order : ExtrinsicRotationOrder | IntrinsicRotationOrder
            Sequence of rotation axes defining the layout of euler_angles.
        axis_orientation : AxisOrientation
            Forward, right, and up Cartesian axes; mapped respectively to roll, pitch, and yaw.

        Returns
        -------
        dict[RotationAxis, int]
            Index in rotation_order for each RotationAxis.
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
        Reorder euler_angles from rotation_order layout to [roll, pitch, yaw].

        Parameters
        ----------
        euler_angles : np.ndarray
            Length-3 array indexed like rotation_order.

        Returns
        -------
        np.ndarray
            Canonical [roll, pitch, yaw] values (same dtype/shape semantics as input elements).
        """
        return np.array([
            euler_angles[self.euler_index_mapper[RotationAxis.ROLL]], 
            euler_angles[self.euler_index_mapper[RotationAxis.PITCH]], 
            euler_angles[self.euler_index_mapper[RotationAxis.YAW]]
            ]
            )