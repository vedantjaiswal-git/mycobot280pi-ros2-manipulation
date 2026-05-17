# Project Overview

## Goal

The project migrated a UR10-based robotics lab course to the smaller MyCobot 280Pi platform. The target stack was Ubuntu 24.04 with ROS 2 Jazzy, Gazebo, RViz2, Python, OpenCV, and YOLO pose estimation.

## Workstreams

| Workstream | Scope |
| --- | --- |
| Shared team platform | MyCobot 280Pi model improvements, URDF/Gazebo setup, controller configuration, joint control in simulation, and shared integration work. |
| Group 1 | Custom hardware/control nodes with forward kinematics, inverse kinematics, joint position control, joint velocity control, and serial communication. |
| Group 2 | Lab PDFs and Jupyter notebook templates/solutions for course migration. Public release should avoid solution material unless approved. |
| Portfolio-owner contribution | Vision-driven pick-and-place package using YOLO/OpenCV cube detection, PnP pose estimation, Z calibration, ROS 2 messages, robot motion, vacuum gripping, color sorting, and stack-height priority. |

## Public Repository Scope

The public repository should contain:

- ROS 2 packages in `src/`.
- High-level documentation in `docs/`.
- Contributor and attribution notes.
- Reproducible setup instructions.

The public repository should not contain:

- `build/`, `install/`, `log/`, `__pycache__/`, or notebook checkpoints.
- Large raw videos, old presentations, zip archives, generated LaTeX files, datasets, or trained model weights.
- Private paths, credentials, personal data, or course solution files.


