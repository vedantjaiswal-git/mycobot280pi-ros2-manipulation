# Simulation

The `mycobot_280_gazebo` package contains the MyCobot 280Pi Gazebo model, URDF, controller configuration, worlds, launch files, and helper scripts. Building the Gazebo simulation package and joint control in simulation was shared work across the student team.

## Build

```bash
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install
source install/setup.bash
```

## Launch Gazebo

```bash
ros2 launch mycobot_280_gazebo mycobot_280_gazebo.launch.py
```

For the launch file that also starts robot-state publishing, controllers, and a clock bridge:

```bash
ros2 launch mycobot_280_gazebo mycobot_280_world.launch.py
```

## Package Contents

```text
mycobot_280_gazebo/
|-- config/
|-- launch/
|-- scripts/
|-- urdf/
`-- worlds/
```

## Notes

- The URDF and controller setup were migrated from a raw semester-project workspace and still need a final Jazzy/Gazebo validation pass.
- Helper scripts use the package-local URDF path instead of machine-specific `/home/...` paths.
- Joint-log helper scripts write to `~/.ros/mycobot_280_gazebo_logs`.

