# axis

## Overview

Single-axis enums for 3D rotations: **intrinsic** axes use uppercase strings (`X`, `Y`, `Z`) and **extrinsic** axes use lowercase (`x`, `y`, `z`), aligned with `scipy.spatial.transform.Rotation` Euler conventions. **`RotationAxis`** names body-style angles (roll, pitch, yaw) for semantic mapping with [`EulerIndexMapper`](../euler/euler_index_mapper.py).

## Example

SciPy-style letters vs semantic body axes:

```python
from handedness_rotation import ExtrinsicAxis3D, IntrinsicAxis3D, RotationAxis

assert IntrinsicAxis3D.Z.value == "Z"
assert ExtrinsicAxis3D.Z.value == "z"

semantic = (RotationAxis.ROLL, RotationAxis.PITCH, RotationAxis.YAW)
```

## Components

| Module | Exports | Description |
| ------ | ------- | ----------- |
| [`intrinsic.py`](./intrinsic.py) | `IntrinsicAxis3D` | Intrinsic rotation axis (one letter per enum member, uppercase value) |
| [`extrinsic.py`](./extrinsic.py) | `ExtrinsicAxis3D` | Extrinsic rotation axis (lowercase value) |
| [`rotation.py`](./rotation.py) | `RotationAxis` | `ROLL`, `PITCH`, `YAW` — used with `EulerIndexMapper` and `AxisOrientation` |
