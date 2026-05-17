import os

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    pkg_ros_gz = FindPackageShare("ros_gz_sim").find("ros_gz_sim")
    pkg_mycobot = FindPackageShare("mycobot_280_gazebo").find("mycobot_280_gazebo")

    # 1️⃣ Start Gazebo with empty world
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [os.path.join(pkg_ros_gz, "launch", "gz_sim.launch.py")]
        ),
        launch_arguments={"gz_args": "-r empty.sdf"}.items(),
    )

    # 2️⃣ Path to URDF with ros2_control tag
    urdf_path = os.path.join(pkg_mycobot, "urdf", "mycobot_280_gazebo.urdf")

    # 3️⃣ Publish URDF to /robot_description
    robot_state_pub = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        parameters=[{"robot_description": open(urdf_path, encoding="utf-8").read()}],
        output="screen",
    )

    # 4️⃣ Spawn robot in Gazebo
    spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=["-file", urdf_path, "-name", "mycobot_280"],
        output="screen",
    )

    # 5️⃣ Spawn controllers
    joint_state_broadcaster = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
        output="screen",
    )

    joint_trajectory_controller = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_trajectory_controller", "--controller-manager", "/controller_manager"],
        output="screen",
    )

    # 6️⃣ Optional: clock bridge (for /clock sync)
    clock_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        name="clock_bridge",
        arguments=["/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock"],
        output="screen",
    )

    return LaunchDescription([
        gazebo,
        robot_state_pub,
        spawn_robot,
        joint_state_broadcaster,
        joint_trajectory_controller,
        clock_bridge,
    ])
