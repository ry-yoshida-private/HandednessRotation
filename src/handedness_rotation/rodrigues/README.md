# rodrigues

## Overview

Rodrigues (axis–angle) vector + **handedness** → `HandednessRotationMatrix`. Skew matrices come from **`rotation`**.

## Components

| Component | Description |
|-----------|-------------|
| [rodrigues_rotation.py](./rodrigues_rotation.py) | `HandednessRodriguesRotationParameter` — axis–angle style vector with handedness; conversion to rotation matrix and vector transform |

`SkewSymmetricMatrix` and the base `RodriguesRotationParameter` (length-3 validation) are defined in **`rotation`** (`rotation.rodrigues`).
