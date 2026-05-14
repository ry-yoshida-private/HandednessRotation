# order

## Overview

Enumerations for **Euler rotation order**: which axis each of the three angles is about. **Intrinsic** orders use **uppercase** labels (`XYZ`, …); **extrinsic** orders use **lowercase** (`xyz`, …), consistent with `scipy.spatial.transform.Rotation`.

These types are the `order` field on [`EulerAngles`](../euler/euler_angles.py) and are iterable like the axis sequence passed to SciPy.

## Example

Iterate to get `cartesian_axis.Axis` values in sequence (for intrinsic, letters stay uppercase; extrinsic enum values are lowercase strings but iteration yields `Axis` with normalized names):

```python
from handedness_rotation import ExtrinsicRotationOrder, IntrinsicRotationOrder

intrinsic_axes = list(IntrinsicRotationOrder.ZYX)
extrinsic_axes = list(ExtrinsicRotationOrder.ZYX)
```

## Components

| Module | Exports | Description |
| ------ | ------- | ----------- |
| [`intrinsic.py`](./intrinsic.py) | `IntrinsicRotationOrder` | Six intrinsic axis sequences |
| [`extrinsic.py`](./extrinsic.py) | `ExtrinsicRotationOrder` | Six extrinsic axis sequences |
