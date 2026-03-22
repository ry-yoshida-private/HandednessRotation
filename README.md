# HandednessRotation

`HandednessRotation` is a Python package for 3D rotations that carries **coordinate handedness** and **axis conventions** alongside matrix, quaternion, and Rodrigues representations.  
It extends [rotation](https://github.com/ry-yoshida-private/Rotation) with `CoordinateHandedness` and `Axis` from [cartesian-axis-3d](https://github.com/ry-yoshida-private/CartesianAxis3D), so quaternions and Rodrigues vectors convert to `HandednessRotationMatrix` with consistent metadata.

## Installation

Install dependencies only:

```bash
pip install -r requirements.txt
```

## Usage

```python
import numpy as np
from cartesian_axis import Axis, CoordinateHandedness

from handedness_rotation import HandednessRotationMatrix

# Right-handed frame: orthogonal 3x3 with determinant +1
R = HandednessRotationMatrix(
    value=np.eye(3),
    coordinate_handedness=CoordinateHandedness.RIGHT,
)

# Column for a named Cartesian axis
x_axis = R.extract_axis_rotation(Axis.X)
```

For module layout (matrix, axis enums, quaternion, Rodrigues), see [`src/handedness_rotation/README.md`](src/handedness_rotation/README.md).
