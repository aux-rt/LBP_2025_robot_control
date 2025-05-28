import keyboard
from lbp_2025_robot_control.config import DynamixelMotorsBusConfig
from lbp_2025_robot_control.dynamixel import DynamixelMotorsBus, TorqueMode
import time


GOAL_SPEED = 40 # Desired speed
motor_idx = None # current motor index, None means no motor selected
motor_goal_vels = [0, 0, 0, 0, 0, 0] # goal velocities for each motor, initialized to 0
stop_robot_flag = False # flag to stop motor


def stop_robot():
    global stop_robot_flag
    stop_robot_flag = True

def change_motor(idx):
    global motor_idx
    motor_idx = idx
    print(f"Motor changed to {motor_idx + 1}")

def set_motor_speed(speed):
    global motor_goal_vels
    if motor_idx is None:
        print("No motor selected")
        return
    motor_goal_vels[motor_idx] = speed
    print(f"Motor {motor_idx + 1} speed set to {speed}")

def reset_motor_speeds():
    global motor_goal_vels
    motor_goal_vels = [0, 0, 0, 0, 0, 0]
    print("All motor speeds reset to 0")


# set up keyboard listeners to change selected motor and set speed
keyboard.on_release_key("1", lambda _: change_motor(0))
keyboard.on_release_key("2", lambda _: change_motor(1))
keyboard.on_release_key("3", lambda _: change_motor(2))
keyboard.on_release_key("4", lambda _: change_motor(3))
keyboard.on_release_key("5", lambda _: change_motor(4))
keyboard.on_release_key("6", lambda _: change_motor(5))
keyboard.on_release_key("0", lambda _: change_motor(None))
keyboard.on_press_key("esc", lambda _: stop_robot())

keyboard.on_press_key("w", lambda _: set_motor_speed(GOAL_SPEED))
keyboard.on_press_key("s", lambda _: set_motor_speed(-GOAL_SPEED))
keyboard.on_release(lambda _: reset_motor_speeds()) # set all motor speeds to 0 when no key is pressed


if __name__ == "__main__":
    follower_config = DynamixelMotorsBusConfig(
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

    follower_arm = DynamixelMotorsBus(follower_config)
    follower_arm.connect()
    print("Connected to follower arm")
    # sét motor control mode to closed loop velocity control
    # all control modes: https://emanual.robotis.com/docs/en/dxl/x/xl330-m288/#operating-mode11
    follower_arm.write("Operating_Mode", 1) # if only one value is passed, it sets all motors to the same mode
    op_mode = follower_arm.read("Operating_Mode")
    print(f"Operating mode set to {op_mode}")

    # enable torque for all motors
    follower_arm.write("Torque_Enable", TorqueMode.ENABLED.value)

    while not stop_robot_flag:
        follower_arm.write("Goal_Velocity", motor_goal_vels)
        cur_vel = follower_arm.read("Present_Velocity")
        cur_pos = follower_arm.read("Present_Position")
        print(f"Current Velocity: {cur_vel}, Goal Velocity: {motor_goal_vels}, Current Position: {cur_pos}")
        time.sleep(0.1)

    print("Stopping robot...")
    follower_arm.write("Goal_Velocity", [0, 0, 0, 0, 0, 0])
    follower_arm.write("Torque_Enable", TorqueMode.DISABLED.value)
