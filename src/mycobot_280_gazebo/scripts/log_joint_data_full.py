#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from control_msgs.msg import JointTrajectoryControllerState
import csv, os
from datetime import datetime

NUM_JOINTS = 6

def pad(arr, n=NUM_JOINTS):
    arr = list(arr)
    if len(arr) >= n:
        return arr[:n]
    return arr + [0.0] * (n - len(arr))

class JointLoggerFull(Node):
    def __init__(self):
        super().__init__("joint_logger_full")

        # === file ===
        log_dir = os.path.expanduser("~/.ros/mycobot_280_gazebo_logs")
        os.makedirs(log_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.file_path = os.path.join(log_dir, f"joint_log_full_{timestamp}.csv")

        self.file = open(self.file_path, "w", newline="")
        self.writer = csv.writer(self.file)

        # === header ===
        header = ["time_sec"]

        header += [f"pos_actual_{i+1}" for i in range(NUM_JOINTS)]
        header += [f"pos_desired_{i+1}" for i in range(NUM_JOINTS)]
        header += [f"pos_error_{i+1}" for i in range(NUM_JOINTS)]

        header += [f"vel_actual_{i+1}" for i in range(NUM_JOINTS)]
        header += [f"vel_desired_{i+1}" for i in range(NUM_JOINTS)]
        header += [f"vel_error_{i+1}" for i in range(NUM_JOINTS)]

        header += [f"effort_output_{i+1}" for i in range(NUM_JOINTS)]

        self.writer.writerow(header)

        # === subscriber ===
        self.create_subscription(
            JointTrajectoryControllerState,
            "/joint_trajectory_controller/controller_state",
            self.callback,
            20
        )

        self.get_logger().info(f"Logging controller state to: {self.file_path}")

    def callback(self, msg):

        t = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9

        # desired (reference)
        pos_d = pad(msg.reference.positions)
        vel_d = pad(msg.reference.velocities)

        # actual (feedback)
        pos_a = pad(msg.feedback.positions)
        vel_a = pad(msg.feedback.velocities)

        # error
        pos_e = pad(msg.error.positions)
        vel_e = pad(msg.error.velocities)

        # controller output effort
        eff_out = pad(msg.output.effort)

        row = (
            [t] +
            pos_a + pos_d + pos_e +
            vel_a + vel_d + vel_e +
            eff_out
        )

        self.writer.writerow(row)

    def destroy_node(self):
        self.file.close()
        self.get_logger().info(f"Saved: {self.file_path}")
        super().destroy_node()


def main():
    rclpy.init()
    node = JointLoggerFull()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
