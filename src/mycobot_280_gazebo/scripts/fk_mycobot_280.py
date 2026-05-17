#!/usr/bin/env python3
"""
Forward Kinematics for MyCobot 280 (ROS2 + IKPy)
Input: six joint angles in degrees
Output: EE position (x, y, z) in meters and orientation (roll, pitch, yaw) in degrees
"""

import numpy as np
import math
from pathlib import Path
from ikpy.chain import Chain

# === Path to your URDF ===
URDF_PATH = str(Path(__file__).resolve().parents[1] / "urdf" / "mycobot_280_gazebo.urdf")

# === Build the chain ===
chain = Chain.from_urdf_file(
    URDF_PATH,
    base_elements=["g_base"],
    active_links_mask=[False, False, True, True, True, True, True, True, False],  # only movable joints
    last_link_vector=[0, 0, -0.012]
)

# === Helper: rotation matrix → roll–pitch–yaw (degrees) ===
def matrix_to_rpy(R):
    roll  = math.atan2(R[2, 1], R[2, 2])
    pitch = math.atan2(-R[2, 0], math.sqrt(R[2, 1] ** 2 + R[2, 2] ** 2))
    yaw   = math.atan2(R[1, 0], R[0, 0])
    return np.rad2deg([roll, pitch, yaw])

# === Main ===
if __name__ == "__main__":
    print("\n--- MyCobot 280 Forward Kinematics ---")
    print("Enter six joint angles (degrees), separated by spaces.")
    print("Order: joint2_to_joint1 joint3_to_joint2 joint4_to_joint3 joint5_to_joint4 joint6_to_joint5 joint6output_to_joint6")

    try:
        angles_deg = list(map(float, input("\nJoint angles [°]: ").split()))
        if len(angles_deg) != 6:
            raise ValueError("You must enter exactly 6 joint angles.")
    except Exception as e:
        print("Invalid input:", e)
        exit(1)

    # Convert to radians
    q_rad = np.deg2rad(angles_deg)

    # Compute FK (skip fixed base joints)
    T = chain.forward_kinematics([0, 0] + q_rad.tolist() + [0])
    pos = T[:3, 3]
    rpy = matrix_to_rpy(T[:3, :3])

    # Display results
    print("\n End-Effector Pose:")
    print(f"Position [m]:  x = {pos[0]:.4f},  y = {pos[1]:.4f},  z = {pos[2]:.4f}")
    print(f"Orientation [°]:  roll = {rpy[0]:.2f},  pitch = {rpy[1]:.2f},  yaw = {rpy[2]:.2f}")
    print("--------------------------------------")
