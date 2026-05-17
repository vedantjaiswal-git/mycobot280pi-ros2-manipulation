# Setup

These notes target Ubuntu 24.04 and ROS 2 Jazzy.

## System Dependencies

```bash
sudo apt update
sudo apt install ros-jazzy-desktop python3-colcon-common-extensions
sudo apt install ros-jazzy-ros-gz ros-jazzy-ros2-control ros-jazzy-ros2-controllers
```

Source ROS 2 before building:

```bash
source /opt/ros/jazzy/setup.bash
```

## Vision Python Environment

The original vision setup used a dedicated Python virtual environment outside the ROS workspace. Install the vision dependencies in that environment before building and running the `vision` package.

```bash
python3 -m venv ~/venvs/mycobot-yolo
source ~/venvs/mycobot-yolo/bin/activate
python -m pip install --upgrade pip
python -m pip install --no-cache-dir \
  ultralytics==8.4.8 \
  torch==2.9.1 torchvision==0.24.1 \
  opencv-python==4.13.0.90 \
  numpy==2.4.1 scipy==1.17.0 \
  matplotlib==3.10.8 pillow==12.1.0 \
  psutil==7.2.1 polars==1.37.1 \
  pyyaml==6.0.3 requests==2.32.5 \
  typing_extensions==4.15.0 typeguard==4.4.4
```

On the MyCobot 280Pi hardware, the motion node also expects:

```bash
pip install pymycobot RPi.GPIO
```

TODO: Validate the pinned vision versions on the final Ubuntu 24.04 / ROS 2 Jazzy machine. If the exact versions are too new for the target hardware, replace them with a tested lock file.

## Build

From the repository root:

```bash
source /opt/ros/jazzy/setup.bash
source ~/venvs/mycobot-yolo/bin/activate
colcon build --symlink-install
source install/setup.bash
```

## Runtime Artifacts Not Committed

The following files are intentionally not committed:

- YOLO model weights such as `best.pt`.
- Training datasets and Ultralytics `runs/` directories.
- Local calibration JSON files.
- Raw videos, old presentations, and raw project archives. Short demo clips and cleaned public report artifacts may be kept under `media/demo/` and `docs/report/`.

Pass the model path to the vision node at runtime:

```bash
ros2 run vision vision_node --ros-args -p model_path:=<path-to-model>/best.pt
```

Optional parameters:

```bash
ros2 run vision vision_node --ros-args \
  -p model_path:=<path-to-model>/best.pt \
  -p camera_device:=/dev/video2 \
  -p calibration_file:=$HOME/.ros/mycobot_z_scale_calibration.json
```

## Hardware Notes

The hardware motion node assumes the MyCobot serial port is available at `/dev/serial0` and uses Raspberry Pi GPIO pins for the vacuum/release hardware. Confirm wiring and emergency-stop procedures before running on the real robot.
