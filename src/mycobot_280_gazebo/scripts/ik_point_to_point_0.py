#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from sensor_msgs.msg import JointState
from ikpy.chain import Chain
import numpy as np
import time, os
from pathlib import Path

URDF_PATH = str(Path(__file__).resolve().parents[1] / "urdf" / "mycobot_280_gazebo.urdf")

class IKMover(Node):
    def __init__(self):
        super().__init__('ik_mover')
        self.pub = self.create_publisher(JointTrajectory,
                                         '/joint_trajectory_controller/joint_trajectory', 10)

        # Build the kinematic chain
        self.chain = Chain.from_urdf_file(URDF_PATH,base_elements=["g_base"],last_link_vector=[0, 0, 0.05])

        self.joint_names = [
            "joint2_to_joint1",
            "joint3_to_joint2",
            "joint4_to_joint3",
            "joint5_to_joint4",
            "joint6_to_joint5",
            "joint6output_to_joint6",
        ]

    def move_to_pose(self, target_pose):
        """
        target_pose = [x, y, z, roll, pitch, yaw]
        """
        # Convert pose to 4x4 transformation matrix
        x, y, z, roll, pitch, yaw = target_pose
        Rz, Ry, Rx = np.deg2rad(yaw), np.deg2rad(pitch), np.deg2rad(roll)
        R = np.array([
            [np.cos(Rz)*np.cos(Ry), np.cos(Rz)*np.sin(Ry)*np.sin(Rx)-np.sin(Rz)*np.cos(Rx), np.cos(Rz)*np.sin(Ry)*np.cos(Rx)+np.sin(Rz)*np.sin(Rx)],
            [np.sin(Rz)*np.cos(Ry), np.sin(Rz)*np.sin(Ry)*np.sin(Rx)+np.cos(Rz)*np.cos(Rx), np.sin(Rz)*np.sin(Ry)*np.cos(Rx)-np.cos(Rz)*np.sin(Rx)],
            [-np.sin(Ry), np.cos(Ry)*np.sin(Rx), np.cos(Ry)*np.cos(Rx)]
        ])
        target_matrix = np.eye(4)
        target_matrix[:3, :3] = R
        target_matrix[:3, 3] = [x, y, z]

        ik_sol = self.chain.inverse_kinematics_frame(target_matrix)
        joint_positions = ik_sol[1:7]   # skip fixed base joint

        traj = JointTrajectory()
        traj.joint_names = self.joint_names
        point = JointTrajectoryPoint()
        point.positions = joint_positions.tolist()
        point.time_from_start.sec = 3
        traj.points = [point]

        self.pub.publish(traj)
        self.get_logger().info(f"Moving to {target_pose}")

def main(args=None):
    rclpy.init(args=args)
    node = IKMover()

    # Example: two poses (units in meters & degrees)
    pose1 = [0.2, 0.0, 0.15, 0, 0, 0]
    pose2 = [0.1, 0.1, 0.2, 0, 0, 90]

    node.move_to_pose(pose1)
    time.sleep(5)
    node.move_to_pose(pose2)

    rclpy.spin(node)

if __name__ == '__main__':
    main()
