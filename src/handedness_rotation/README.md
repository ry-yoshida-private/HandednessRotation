# handedness_rotation

## Overview

Adds **left/right-handed** coordinates and axis naming on top of [rotation](https://github.com/ry-yoshida-private/Rotation). Quaternions and Rodrigues vectors become `HandednessRotationMatrix` with the same handedness.

Uses **rotation** (rotations) and **cartesian-axis-3d** (`CoordinateHandedness`, `Axis`).

## Components


| Component                             | Description                                                                                                                         |
| ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| [matrix.py](./matrix.py)              | `HandednessRotationMatrix` — extends `RotationMatrix` with handedness, axis extraction, composition rules, QR/SVD orthogonalization |
| [axis/](./axis/README.md)             | Intrinsic / extrinsic axis enums for scipy Euler strings, plus roll–pitch–yaw labels                                                |
| [quaternion/](./quaternion/README.md) | `HandednessQuaternion` — quaternion + handedness; matrix conversion                                                                 |
| [rodrigues/](./rodrigues/README.md)   | `HandednessRodriguesRotationParameter` — Rodrigues vector + handedness; uses `SkewSymmetricMatrix` from `rotation`                  |


