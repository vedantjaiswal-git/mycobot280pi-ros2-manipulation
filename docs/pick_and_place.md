# Pick And Place

The pick-and-place application was the primary portfolio-owner contribution in the group project. The Gazebo simulation package and joint control in simulation were shared team work.

## Pipeline

1. A USB camera captures the workspace.
2. A YOLO pose model detects cube classes and keypoints.
3. OpenCV `solvePnP` estimates cube pose from image keypoints and cube geometry.
4. A Z-scale calibration step maps raw PnP depth to robot-base height.
5. The `vision` node publishes `mycobot_msgs/DetectedObject` messages on `/detected_objects`.
6. The `mycobot_motion_v1` node filters detections by workspace limits, waits briefly to collect candidates, chooses the highest-priority target, and commands pick-and-place motion.
7. A vacuum output is toggled during grasp/release.
8. Cubes are sorted into color-specific bins.

## ROS Interface

Published by `vision`:

```text
/detected_objects  mycobot_msgs/msg/DetectedObject
```

Message fields:

```text
float32 x
float32 y
float32 z
string color
```

Consumed by `mycobot_motion_v1`:

```bash
ros2 run mycobot_motion_v1 motion_node
```

## Vision Node

Run with an external model path:

```bash
ros2 run vision vision_node --ros-args -p model_path:=<path-to-model>/best.pt
```

The model weights are not committed because trained weights can be large, may depend on dataset licensing, and are better published as a release artifact only after review.

## Calibration

The vision node stores Z calibration data in:

```text
~/.ros/mycobot_z_scale_calibration.json
```

If no calibration file exists, the node enters an interactive calibration mode. The user places a cube in the workspace and captures multiple samples.

## Target Priority

The motion node prioritizes:

- Higher stacks first, based on the published Z value.
- Color priority as a tiebreaker: red, yellow, green, cyan.
