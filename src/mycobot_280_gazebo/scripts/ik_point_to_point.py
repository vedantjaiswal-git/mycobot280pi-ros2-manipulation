#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint
from ikpy.chain import Chain
import numpy as np
from pathlib import Path

URDF_PATH = str(Path(__file__).resolve().parents[1] / "urdf" / "mycobot_280_gazebo.urdf")


class IKMover(Node):
    def __init__(self):
        super().__init__("ik_mover_safe")

        # Build kinematic chain from URDF
        self.chain = Chain.from_urdf_file(
            URDF_PATH,
            base_elements=["g_base"],
            last_link_vector=[0, 0, 0.05]
        )

        # Define actuated joints (ROS2 controller order)
        self.joint_names = [
            "joint2_to_joint1",
            "joint3_to_joint2",
            "joint4_to_joint3",
            "joint5_to_joint4",
            "joint6_to_joint5",
            "joint6output_to_joint6",
        ]

        # Full-length IK seed (1 value per link)
        self.prev_q_full = np.zeros(len(self.chain.links))

        # Disable fixed joints in the mask to quiet warnings
        mask = [True] * len(self.chain.links)
        mask[0] = False  # "Base link"
        mask[1] = False  # "g_base_to_joint1" (fixed)
        mask[-1] = False  # "last_joint" (fixed)
        self.chain.active_links_mask = mask

        # Action client to the trajectory controller
        self.client = ActionClient(
            self,
            FollowJointTrajectory,
            "/joint_trajectory_controller/follow_joint_trajectory",
        )

    # ------------------------------------------------------------------
    def pose_to_matrix(self, pose):
        """Convert [x, y, z, roll, pitch, yaw] in degrees to a 4x4 transform."""
        x, y, z, roll, pitch, yaw = pose
        roll, pitch, yaw = np.deg2rad([roll, pitch, yaw])

        Rz, Ry, Rx = yaw, pitch, roll
        R = np.array([
            [np.cos(Rz) * np.cos(Ry),
             np.cos(Rz) * np.sin(Ry) * np.sin(Rx) - np.sin(Rz) * np.cos(Rx),
             np.cos(Rz) * np.sin(Ry) * np.cos(Rx) + np.sin(Rz) * np.sin(Rx)],
            [np.sin(Rz) * np.cos(Ry),
             np.sin(Rz) * np.sin(Ry) * np.sin(Rx) + np.cos(Rz) * np.cos(Rx),
             np.sin(Rz) * np.sin(Ry) * np.cos(Rx) - np.cos(Rz) * np.sin(Rx)],
            [-np.sin(Ry),
             np.cos(Ry) * np.sin(Rx),
             np.cos(Ry) * np.cos(Rx)]
        ])
        T = np.eye(4)
        T[:3, :3] = R
        T[:3, 3] = [x, y, z]
        return T

    # ------------------------------------------------------------------
    def interpolate(self, start, end, steps):
        """Generate evenly spaced intermediate poses."""
        return [
            [start[j] + (end[j] - start[j]) * i / steps for j in range(6)]
            for i in range(steps + 1)
        ]

    # ------------------------------------------------------------------
    def move_linear(self, start_pose, end_pose, total_time=10.0, steps=40):
        """Compute and send a smooth trajectory between two poses."""
        poses = self.interpolate(start_pose, end_pose, steps)
        self.client.wait_for_server()

        goal = FollowJointTrajectory.Goal()
        goal.trajectory.joint_names = self.joint_names

        dt = total_time / steps
        for i, pose in enumerate(poses):
            T = self.pose_to_matrix(pose)

            # Full-length IK seed and storage
            ik_sol_full = self.chain.inverse_kinematics_frame(
                T, initial_position=self.prev_q_full
            )
            self.prev_q_full = ik_sol_full
            q = ik_sol_full[1:7]  # six revolute joints

            point = JointTrajectoryPoint()
            point.positions = q.tolist()

            # Gentle ramp-up delay to prevent jumps
            t = 2.0 + i * dt
            point.time_from_start.sec = int(t)
            point.time_from_start.nanosec = int((t % 1) * 1e9)
            goal.trajectory.points.append(point)

        self.get_logger().info(
            f"Sending smooth trajectory ({steps} steps, {total_time:.1f}s)..."
        )
        send_future = self.client.send_goal_async(goal, feedback_callback=self.feedback_cb)
        rclpy.spin_until_future_complete(self, send_future)
        goal_handle = send_future.result()

        if not goal_handle or not goal_handle.accepted:
            self.get_logger().error("Goal rejected by controller.")
            return

        rclpy.spin_until_future_complete(self, goal_handle.get_result_async())
        self.get_logger().info("Motion completed successfully.")

    # ------------------------------------------------------------------
    def feedback_cb(self, feedback_msg):
        """Receive and log joint angle feedback (degrees)."""
        if hasattr(feedback_msg.feedback, "actual"):
            pos = np.degrees(feedback_msg.feedback.actual.positions)
            pos = np.round(pos, 1)
            self.get_logger().info(f"Joint feedback [°]: {pos.tolist()}")


# ----------------------------------------------------------------------
def main():
    rclpy.init()
    node = IKMover()

    # Example: safe two-pose motion
    pose1 = [0.18, 0.0, 0.14, 0, 0, 0]
    pose2 = [0.12, 0.10, 0.18, 0, 0, 60]

    node.move_linear(pose1, pose2, total_time=10.0, steps=50)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
