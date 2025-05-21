from src.lbp_2025_robot_control.dynamixel import DynamixelMotorsBus, TorqueMode
import time
import keyboard
from src.lbp_2025_robot_control.config import DynamixelMotorsBusConfig, KochRobotConfig
from src.lbp_2025_robot_control.manipulator import ManipulatorRobot, create_koch_robot
import numpy as np

VEL = 50
torque_enabled = False
stored_pos = []
curr_index = 0

def load_positions():
    try:
        with open("taught_positions.txt", "r") as f:
            stored_pos_tmp = [np.array(list(map(float, line.strip()[1:-2].split()))) for line in f]
            for i in range(len(stored_pos_tmp)):
                for j in range(len(stored_pos_tmp[i])):
                    if stored_pos_tmp[i][j] > 190:
                        stored_pos_tmp[i][j] = stored_pos_tmp[i][j] - 180
                    elif stored_pos_tmp[i][j] < -190:
                        stored_pos_tmp[i][j] = stored_pos_tmp[i][j] + 180

        # if len(stored_pos_tmp) > 5:
        #     raise ValueError("Invalid number of positions in positions.txt. Expected < 4.")
        # if len(stored_pos_tmp) < 5:
        #     stored_pos_tmp += [None] * (5 - len(stored_pos_tmp))
        print(f"Positions loaded from positions.txt: {stored_pos_tmp}")
        print(f"{len(stored_pos_tmp)} positions loaded")
        return stored_pos_tmp
    except FileNotFoundError:
        print("positions.txt not found. No positions loaded.")
        return []

def toggle_torque():
    global torque_enabled
    torque_enabled = not torque_enabled
    if torque_enabled:
        follower_arm.write("Torque_Enable", TorqueMode.ENABLED.value)
        print("Torque enabled")
    else:
        follower_arm.write("Torque_Enable", TorqueMode.DISABLED.value)
        print("Torque disabled")

def add_pos():
    global stored_pos
    new_pos = follower_arm.read("Present_Position")
    stored_pos.append(new_pos)
    print(f"Added new position: {new_pos}")

def remove_last_pos():
    global stored_pos
    if stored_pos:
        removed_pos = stored_pos.pop()
        print(f"Removed last position: {removed_pos}")

def drive_to_next_pos():
    global curr_index, stored_pos
    if curr_index >= len(stored_pos):
        print("No more positions to drive to")
        return
    follower_arm.write("Goal_Position", stored_pos[curr_index])
    print(f"Driving to position {curr_index + 1}: {stored_pos[curr_index]}")
    curr_index += 1

def drive_to_last_pos():
    global curr_index, stored_pos
    curr_index -= 1
    if curr_index < 0:
        print("No more positions to drive to")
        return
    follower_arm.write("Goal_Position", stored_pos[curr_index])
    print(f"Driving to position {curr_index + 1}: {stored_pos[curr_index]}")


def reset_index():
    global curr_index
    curr_index = 0

def export_positions():
    global stored_pos
    with open("taught_positions.txt", "w") as f:
        for pos in stored_pos:
            if pos is not None:
                f.write(f"{pos}\n")
    print("Positions exported to taught_positions.txt")


stored_pos = load_positions()
print(stored_pos)


if __name__ == "__main__":
    robot = create_koch_robot("COM3")
    robot.connect()
    follower_arm = robot.follower_arms["main"]


    print("Connected to follower arm")
    follower_arm.write("Velocity_Limit", [VEL, VEL, VEL, VEL, VEL, VEL])
    vel_limit = follower_arm.read("Velocity_Limit")
    print(vel_limit)
    op_mode = follower_arm.read("Operating_Mode")
    print(op_mode)
    # follower_arm.write("Operating_Mode", 4) # set to position mode^111
    # op_mode = follower_arm.read("Operating_Mode")
    print(op_mode)
    follower_arm.write("Profile_Velocity", [VEL, VEL, VEL, VEL, VEL, VEL])
    follower_arm.write("Torque_Enable", TorqueMode.DISABLED.value)

    keyboard.on_release_key("t", lambda _: toggle_torque())
    keyboard.on_release_key("-", lambda _: remove_last_pos())
    keyboard.on_release_key("0", lambda _: reset_index())
    keyboard.on_release_key("+", lambda _: add_pos())
    keyboard.on_release_key("d", lambda _: drive_to_next_pos())
    keyboard.on_release_key("l", lambda _: drive_to_last_pos())
    keyboard.on_release_key("s", lambda _: export_positions())
    # keyboard.on_release_key("7", lambda _: drive_to_pos(1))^11111121
    # keyboard.on_release_key("8", lambda _: drive_to_pos(2))
    # keyboard.on_release_key("9", lambda _: drive_to_pos(3))
    # keyboard.on_release_key("0", lambda _: drive_to_pos(4))
    # keyboard.on_release_key("ß", lambda _: export_positions())
    # keyboard.wait("esc")
    # follower_arm.write("Torque_Enable", TorqueMode.DISABLED.value)
    # follower_arm.write("Homing_Offset", [0, 0, 0, 0, 0, 0])
    print("Homing offset:")
    print(follower_arm.read("Homing_Offset"))
    # print("_________")


    max_pos_limits = [4095, 4095, 4095, 4095, 4095, 4095]
    min_pos_limits = [0, 0, 0, 0, 0, 0]
    follower_arm.write("Max_Position_Limit", max_pos_limits)
    follower_arm.write("Min_Position_Limit", min_pos_limits)
    print(f"Max position limits: {follower_arm.read('Max_Position_Limit')}")
    print(f"Min position limits: {follower_arm.read('Min_Position_Limit')}")

    while True:
        cur_pos = follower_arm.read("Present_Position")
        print(f"Current position: [{", ".join(map(str, list((cur_pos))))}]")
        time.sleep(0.5)
