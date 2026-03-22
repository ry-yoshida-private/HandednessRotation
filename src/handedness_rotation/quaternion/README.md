# quaternion

## Overview

Quaternion + **handedness** on top of `rotation`’s `Quaternion` / `QuaternionFormat` (WXYZ or XYZW). Converts to `HandednessRotationMatrix`.

## Components

| Component | Description |
|-----------|-------------|
| [container.py](./container.py) | `HandednessQuaternion` — normalized quaternion with format and `CoordinateHandedness`; conversion to rotation matrix |

`QuaternionFormat` and the base `Quaternion` validation live in the **`rotation`** package (`rotation.quaternion.format`, `rotation.quaternion.container`).
