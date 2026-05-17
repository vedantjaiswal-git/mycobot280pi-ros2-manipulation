#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from control_msgs.msg import JointTrajectoryControllerState
from message_filters import Subscriber, ApproximateTimeSynchronizer
import csv, os
from datetime import datetime

class JointLoggerFused(Node):
    def __init__(self):
        super().__init__('joint_logger_fused')

        # === Folder setup ===
        log_dir = os.path.expanduser('~/.ros/mycobot_280_gazebo_logs')
        os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.file_path = os.path.join(log_dir, f'joint_log_fused_{timestamp}.csv')

        # === CSV file ===
        self.file = open(self.file_path, 'w', newline='')
        self.writer = csv.writer(self.file)

        header = (
            ['time_sec'] +
            [f'pos_actual_{i+1}' for i in range(6)] +
            [f'pos_desired_{i+1}' for i in range(6)] +
            [f'pos_error_{i+1}' for i in range(6)] +
            [f'vel_actual_{i+1}' for i in range(6)] +
            [f'effort_actual_{i+1}' for i in range(6)]
        )
        self.writer.writerow(header)

        # === Message filters subscribers ===
        self.js_sub = Subscriber(self, JointState, '/joint_states')
        self.ctrl_sub = Subscriber(self, JointTrajectoryControllerState,
                                   '/joint_trajectory_controller/controller_state')

        # === Approximate sync ===
        self.sync = ApproximateTimeSynchronizer(
            [self.js_sub, self.ctrl_sub],
            queue_size=50,
            slop=0.05     # 50 ms tolerance
        )
        self.sync.registerCallback(self.synced_callback)

        self.get_logger().info(f"🔥 Logging fused joint data to:\n{self.file_path}")

    def synced_callback(self, js_msg, ctrl_msg):
        # --- Time ---
        t = js_msg.header.stamp.sec + js_msg.header.stamp.nanosec * 1e-9

        # --- Actual joint states (/joint_states) ---
        pos_actual = list(js_msg.position[:6])
        vel_actual = list(js_msg.velocity[:6])
        effort_actual = list(js_msg.effort[:6])

        # --- Controller state (/controller_state) ---
        pos_des = list(ctrl_msg.reference.positions[:6])
        pos_fb = list(ctrl_msg.feedback.positions[:6])
        pos_err = list(ctrl_msg.error.positions[:6])

        # (Note: desired velocity/effort are usually empty in position controller)

        row = (
            [t] +
            pos_fb +          # actual positions
            pos_des +         # desired positions
            pos_err +         # errors
            vel_actual +      # actual velocities
            effort_actual     # actual efforts
        )

        self.writer.writerow(row)

    def destroy_node(self):
        self.file.close()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = JointLoggerFused()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
