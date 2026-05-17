cmake_minimum_required(VERSION 3.8)
project(mycobot_280_gazebo)

find_package(ament_cmake REQUIRED)
find_package(ros_gz_sim REQUIRED)
find_package(ros_gz_bridge REQUIRED)
find_package(ros2_control REQUIRED)
find_package(ros2_controllers REQUIRED)
find_package(xacro REQUIRED)
find_package(ros_gz REQUIRED)

install(DIRECTORY config launch urdf worlds
  DESTINATION share/${PROJECT_NAME}/
)

install(PROGRAMS
  scripts/move_mycobot.py
  scripts/log_joint_data.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
