from __future__ import annotations

from types import NotImplementedType
from typing import Generic, TypeVar, cast

from rotation import RotationMatrix as R

from ..protocol import HandedRotationMatrixCls, HandedRotationMatrixProtocol

_TSpecial = TypeVar("_TSpecial", bound=HandedRotationMatrixProtocol)


class RotationMatrixSpecialMixin(Generic[_TSpecial]):
    """Dunder behavior for this package's handedness matrix type (e.g. @ composition)."""

    def __matmul__(self: _TSpecial, other: object) -> _TSpecial | NotImplementedType:
        """
        Multiply two handedness rotation matrices.

        Parameters
        ----------
        other : object
            Right-hand operand; must be this package's RotationMatrix with matching handedness.

        Returns
        -------
        RotationMatrix:
            The matrix product, with the same coordinate_handedness as self.

        Raises
        ------
        TypeError:
            If other is not a RotationMatrix.
        ValueError:
            If other is a handedness RotationMatrix but coordinate_handedness differs from self.
        """
        typ = type(self)
        ctor = cast(HandedRotationMatrixCls[_TSpecial], typ)
        if isinstance(other, typ):
            if other.coordinate_handedness == self.coordinate_handedness:
                return ctor(
                    value=self.value @ other.value,
                    coordinate_handedness=self.coordinate_handedness,
                )
            raise ValueError(
                "Cannot compose rotations with different coordinate_handedness tags."
            )
        if isinstance(other, R):
            raise TypeError(
                "RotationMatrix @ other requires another handedness RotationMatrix; use plain RotationMatrix @ RotationMatrix from the base package if handedness is not needed."
            )
        return NotImplemented
