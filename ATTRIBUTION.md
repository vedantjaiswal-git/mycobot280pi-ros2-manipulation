# Attribution

This repository is a cleaned public portfolio version of a six-student master's semester project.

## Project Code

Unless otherwise noted, project code in this repository is released under the MIT License.

## Robot Model Assets

The MyCobot 280Pi mesh and URDF assets in `src/mycobot_description` are included to make the Gazebo simulation reproducible. These assets describe an Elephant Robotics MyCobot 280Pi platform and may be derived from vendor or community robot-description resources. Verify the original asset license before redistributing modified mesh assets outside this portfolio repository.

## Third-Party Software

- ROS 2 Jazzy and Gazebo are used for middleware, simulation, launch, and control integration.
- OpenCV is used for image processing and PnP pose estimation.
- Ultralytics YOLO is used for pose-model inference. Model weights are intentionally not committed.
- `pymycobot` and Raspberry Pi GPIO libraries are used for hardware-side robot and vacuum control.

## Academic Context

The repository documents a group semester project. Contributor names, course material, solution files, datasets, and trained weights should only be published with the appropriate permissions.
