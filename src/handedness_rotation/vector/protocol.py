from __future__ import annotations

from typing import Protocol, TypeVar, cast

import numpy as np
from cartesian_axis import CoordinateHandedness
from rotation.vector.protocol import RotationVectorLike


class HandedRotationVectorProtocol(RotationVectorLike, Protocol):
    """Structural surface for vector mixins (extends upstream ``RotationVectorLike``)."""

    coordinate_handedness: CoordinateHandedness

    def __init__(
        self,
        *,
        value: np.ndarray,
        coordinate_handedness: CoordinateHandedness,
    ) -> None: ...


THandedVectorOut = TypeVar(
    "THandedVectorOut",
    bound=HandedRotationVectorProtocol,
    covariant=True,
)


class HandedRotationVectorCls(Protocol[THandedVectorOut]):
    def __call__(
        self,
        *,
        value: np.ndarray,
        coordinate_handedness: CoordinateHandedness,
    ) -> THandedVectorOut: ...


_SubclassHanded = TypeVar("_SubclassHanded", bound=HandedRotationVectorProtocol)


def handed_rotation_vector_ctor(
    cls: type[_SubclassHanded],
) -> HandedRotationVectorCls[_SubclassHanded]:
    return cast(HandedRotationVectorCls[_SubclassHanded], cls)
