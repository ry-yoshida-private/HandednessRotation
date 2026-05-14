# euler

## Overview

**Euler angle** utilities: a tagged triple (`EulerAngles`) compatible with SciPy-style intrinsic/extrinsic multiplication order, and **`EulerIndexMapper`** to relate storage order to semantic roll / pitch / yaw using `AxisOrientation`.

## Example

`EulerAngles` holds a length-3 `value`, an intrinsic or extrinsic `order`, and a `units.AngleUnit`. The `rotation_matrix` property composes single-axis steps (same convention as SciPy). `EulerIndexMapper` reorders `value` into `[roll, pitch, yaw]` using `AxisOrientation` (forward / right / up from `cartesian_axis`).

```python
import numpy as np
from cartesian_axis import Axis, AxisOrientation
from units import AngleUnit

from handedness_rotation import EulerAngles, EulerIndexMapper, IntrinsicRotationOrder

euler = EulerAngles(
    value=np.array([5.0, 10.0, 15.0], dtype=np.float64),
    order=IntrinsicRotationOrder.ZYX,
    unit=AngleUnit.DEGREE,
)
R = euler.rotation_matrix  # (3, 3) float64, composed per order / unit

mapper = EulerIndexMapper(
    rotation_order=euler.order,
    axis_orientation=AxisOrientation(
        forward=Axis.X,
        right=Axis.Y,
        up=Axis.Z,
    ),
)
roll_pitch_yaw = mapper(euler.value)  # shape (3,), semantic [roll, pitch, yaw]
```

## Components

| Module | Description |
| ------ | ----------- |
| [`euler_angles.py`](./euler_angles.py) | `EulerAngles` — `value` shape `(3,)`, `order` (`IntrinsicRotationOrder` \| `ExtrinsicRotationOrder`), `unit` (`AngleUnit`); `rotation_matrix` composes steps with right-handed axis–angle steps per convention |
| [`euler_index_mapper.py`](./euler_index_mapper.py) | `EulerIndexMapper` — maps `RotationAxis` to indices for a given `rotation_order`, and reorders angle vectors to `[roll, pitch, yaw]` |

Depends on [`../matrix`](../matrix/README.md), [`../order`](../order/README.md), and [`../axis`](../axis/README.md) (`RotationAxis`).
