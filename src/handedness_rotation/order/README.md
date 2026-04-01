# rotation_order

## Overview

This module provides enumerations for rotation orders used in Euler angle representations. <br>
It supports both intrinsic and extrinsic rotation orders, with uppercase for intrinsic and lowercase for extrinsic to match scipy.spatial.transform.Rotation conventions.

## Components

| Component | Description |
|-----------|-------------|
| [intrinsic.py](./intrinsic.py) | Enumeration for intrinsic rotation orders (XYZ, XZY, YXZ, YZX, ZXY, ZYX) with uppercase representation |
| [extrinsic.py](./extrinsic.py) | Enumeration for extrinsic rotation orders (xyz, xzy, yxz, yzx, zxy, zyx) with lowercase representation |
