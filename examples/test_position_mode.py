from lbp_2025_robot_control.dynamixel import DynamixelMotorsBus, TorqueMode
import time
import keyboard
from lbp_2025_robot_control.config import DynamixelMotorsBusConfig, KochRobotConfig
from lbp_2025_robot_control.manipulator import ManipulatorRobot
import numpy as np

VEL = 40
POSITIONS = [np.array([99.140625, 61.875, 47.90039, 92.46094, 88.50586, 4.833980]),
             np.array([24.521484, 62.314453, 41.220703, 92.72461, 88.41797, 4.83398]),
             np.array([-28.300781, 97.99805, 92.021484, 102.91992, -87.36328, 4.57031])]
curr_index = 0
stop_robot_flag = False # flag to stop motor

def stop_robot():
    global stop_robot_flag
    stop_robot_flag = True

def drive_to_next_pos():
    global curr_index
    if curr_index >= len(POSITIONS):
        print("No more positions to drive to")
        return
    follower_arm.write("Goal_Position", POSITIONS[curr_index])
    print(f"Driving to position {curr_index + 1}: {POSITIONS[curr_index]}")
    curr_index += 1

keyboard.on_press_key("esc", lambda _: stop_robot())
keyboard.on_release_key("n", lambda _: drive_to_next_pos())

if __name__ == "__main__":
    follower_config = DynamixelMotorsBusConfig(
        # change to your port:
        # run `python venv\Lib\site-packages\lbp_2025_robot_control\find_motors_bus_port.py` in the terminal to find the port
        port="COM3", 
        motors={
            # name: (index, model)
            "shoulder_pan": (1, "xl430-w250"),
            "shoulder_lift": (2, "xl430-w250"),
            "elbow_flex": (3, "xl330-m288"),
            "wrist_flex": (4, "xl330-m288"),
            "wrist_roll": (5, "xl330-m288"),
            "gripper": (6, "xl330-m288"),
        },
    )
    robot_config = KochRobotConfig(
        leader_arms={},
        follower_arms={"main": follower_config},
        cameras={},  # We don't use any camera for now
    )
    robot = ManipulatorRobot(robot_config)
    robot.connect()
    follower_arm = robot.follower_arms["main"]

    print("Connected to follower arm")

    # set velocity for point-to-point motion
    # be carful with the velocity, the robot can move very fast if you remove this or set it too high.
    follower_arm.write("Profile_Velocity", [VEL, VEL, VEL, VEL, VEL, VEL]) 
    follower_arm.write("Torque_Enable", TorqueMode.ENABLED.value)
    error_counter = 0
    # print the current motor positions
    while not stop_robot_flag and error_counter < 5:
        # catch connection error if only happens once in a while
        try:
            cur_pos = follower_arm.read("Present_Position")
            print(f"Current position: [{", ".join(map(str, list((cur_pos))))}]")
        except ConnectionError as e:
            error_counter += 1
            print(f"Connection error: {e}. Retrying... ({error_counter})")
        time.sleep(0.5)

    print("Stopping robot...")
    follower_arm.write("Goal_Velocity", [0, 0, 0, 0, 0, 0])
    follower_arm.write("Torque_Enable", TorqueMode.DISABLED.value)
