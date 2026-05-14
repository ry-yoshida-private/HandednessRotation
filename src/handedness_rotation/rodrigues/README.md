# rodrigues

## Overview

**`RodriguesRotationParameter`** extends `rotation.RodriguesRotationParameter` with **`coordinate_handedness`**. The length-3 Rodrigues vector and conversion to a 3×3 rotation matrix follow **`rotation`**; handedness is a convention tag on the container.

## Example

`value` is a length-3 array; **`rotation`** uses its norm as the rotation angle (radians) and its direction as the axis. `transform` applies the same matrix as `rotation_matrix @ vector`.

```python
import numpy as np
from cartesian_axis import CoordinateHandedness

from handedness_rotation import RodriguesRotationParameter

h = CoordinateHandedness.RIGHT
theta = np.pi / 2
k = RodriguesRotationParameter(
    value=np.array([0.0, 0.0, theta], dtype=np.float64),
    coordinate_handedness=h,
)
R = k.rotation_matrix  # (3, 3)
v = k.transform(np.array([1.0, 0.0, 0.0]))
```

## Components

| Module | Description |
| ------ | ----------- |
| [`rodrigues_rotation.py`](./rodrigues_rotation.py) | `RodriguesRotationParameter` — axis–angle style vector + handedness |

`SkewSymmetricMatrix` and the base Rodrigues parameter type are defined in **`rotation`** (`rotation.rodrigues`).
