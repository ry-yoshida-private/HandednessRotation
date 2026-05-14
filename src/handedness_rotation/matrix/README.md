# matrix

## Overview

**`RotationMatrix`** is a frozen dataclass: a proper 3×3 rotation matrix (from `rotation.RotationMatrix`) plus **`coordinate_handedness`**. It adds axis column extraction, factories, optional handedness relabeling, and **`@`** multiplication that requires the same handedness on both operands.

## Example

Factories take `coordinate_handedness`; **`@`** composes two matrices only when both operands share the same tag. `extract_axis_rotation` returns the column for a Cartesian `Axis`.

```python
import numpy as np
from cartesian_axis import Axis, CoordinateHandedness

from handedness_rotation import RotationMatrix

h = CoordinateHandedness.RIGHT
R_z = RotationMatrix.from_axis_angle(Axis.Z, np.pi / 6, coordinate_handedness=h)
R_y = RotationMatrix.from_axis_angle(Axis.Y, np.pi / 4, coordinate_handedness=h)
R = R_z @ R_y

x_body = R.extract_axis_rotation(Axis.X)  # shape (3,)
```

## Layout

| Piece | Role |
| ----- | ---- |
| [`base.py`](./base.py) | `RotationMatrix` dataclass and `extract_axis_rotation` |
| [`protocol.py`](./protocol.py) | Protocols and constructors used by mixins |
| [`mixin/convert.py`](./mixin/convert.py) | Conversions (e.g. opposite-handedness tag, Euler-related helpers) |
| [`mixin/factory.py`](./mixin/factory.py) | Classmethods: identity, from approximate matrix (QR/SVD), axis–angle, etc. |
| [`mixin/special.py`](./mixin/special.py) | `__matmul__` and related special behavior |

Mixins are kept plain (not subclassing upstream factory mixins) to avoid MRO clashes with **`rotation`**; they are composed on the final `RotationMatrix` class in `base.py`.
