#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import csv, os
from datetime import datetime

class JointLogger(Node):
    def __init__(self):
        super().__init__('joint_logger')

        # === Folder setup ===
        log_dir = os.path.expanduser('~/.ros/mycobot_280_gazebo_logs')
        os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.file_path = os.path.join(log_dir, f'joint_log_{timestamp}.csv')

        # === CSV setup ===
        self.file = open(self.file_path, 'w', newline='')
        self.writer = csv.writer(self.file)

        # Header: time + 18 joint fields
        header = (
            ['time_sec'] +
            [f'q{i+1}' for i in range(6)] +
            [f'qd{i+1}' for i in range(6)] +
            [f'tau{i+1}' for i in range(6)]
        )
        self.writer.writerow(header)

        # === ROS subscriber ===
        self.create_subscription(JointState, '/joint_states', self.callback, 20)

        self.get_logger().info(f'Logging joint data to: {self.file_path}')

    def callback(self, msg):
        t = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9
        n = len(msg.name)

        # Pad or trim to 6 joints in case the message varies
        q = list(msg.position[:6]) + [0.0] * (6 - n)
        qd = list(msg.velocity[:6]) + [0.0] * (6 - n)
        tau = list(msg.effort[:6]) + [0.0] * (6 - n)

        # One single row per timestamp
        self.writer.writerow([t] + q + qd + tau)

    def destroy_node(self):
        self.file.close()
        self.get_logger().info('Log file saved.')
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = JointLogger()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Logging stopped by user.')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
