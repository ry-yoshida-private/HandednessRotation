# quaternion

## Overview

**`Quaternion`** extends `rotation.Quaternion` with a **`coordinate_handedness`** field. Format (`WXYZ` / `XYZW`) and normalization rules come from **`rotation`**; the handedness tag is metadata and does not change the inherited `rotation_matrix` computation.

## Example

`value` must be shape `(4,)` and **normalized** (same checks as **`rotation`**). `QuaternionFormat` comes from **`rotation`**.

```python
import numpy as np
from cartesian_axis import CoordinateHandedness
from rotation import QuaternionFormat

from handedness_rotation import Quaternion

h = CoordinateHandedness.RIGHT
q = Quaternion(
    value=np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float64),
    format=QuaternionFormat.WXYZ,
    coordinate_handedness=h,
)
R = q.rotation_matrix  # (3, 3), SciPy convention via rotation.Quaternion
```

## Components

| Module | Description |
| ------ | ----------- |
| [`container.py`](./container.py) | `Quaternion` — frozen dataclass with `value`, `format`, `coordinate_handedness` |

Base types `QuaternionFormat` and validation live in **`rotation`** (`rotation.quaternion`).
