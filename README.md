# MOTION CONTROL FOR THE LBP 2025 Robot @ University of Augsburg
## Installation
### 1.  Install Python 3.12 if needed
    1. Go to: https://www.python.org/downloads/release/python-3129/ and download the version corresponding to your system.
    2. Install it and make sure to check the boxes that say:  
        "Add Python to PATH" and "Remove path maximum path length" (on Windows)
 ### 2. Create a virtual environment
In your project directory, run the following:
```
# Create a virtual environment named 'venv'
python -m venv venv

# Activate the virtual environment:
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```
### 3. Install dependencies
Install the necessary dependencies with pip:
```
pip install git+https://github.com/aux-rt/LBP_2025_robot_control
```

### 4. Download Examples
Download the two files in the `examples` folder on GitHub and put them in your working directory (next to your venv folder).

## Robot Arm Setup Tutorial
### 1. Identify Your COM Port

Check the name of your COM port by running:

```
find_motors_bus_port
```


### 2. Assign Unique Motor IDs

Start with the motor at the **base** and work your way to the **gripper**. To change the ID of a motor:

1. **Unplug all motors except the one whose ID you want to change.**

2. ⚠️ **Caution:** Do **not** connect 5V motors (`xl330`) to a 12V power supply. This will **damage** the motors.

3. With only the target motor plugged in, run the following script (update the port if needed):

```
configure_motor.py --port /dev/tty.usbmodem58760432961 --model xl330-m288 --baudrate 1000000 --ID 1
```

- Use model `xl430-w250` for the **first two motors** (12V).
- Use model `xl330-m288` for the **remaining motors** (5V).
- Assign **ID 1–6**, starting from the base and ending at the gripper.

### 3. Test Motors in Velocity Mode

Run the test script:

```
python test_velocity_mode.py
```

- Select a motor by pressing keys **1–6**.
- Rotate the selected motor using **'w'** and **'s'**.
- Press **'ESC'** to exit. Be careful as the torque is disabled and the robot will collapse.

🎉 If motors respond correctly, your robot is working!


### 4. Calibrate the Motors (One-Time Setup)

To allow motors to return to the same position after being unplugged, perform a **calibration**:

1. Run:

```
python test_position_mode.py
```

2. If no calibration data is found, the program will prompt you to move each motor to various orientations.

   - 📸 The terminal will display links to example images showing the required poses.

3. After the procedure, calibration data is saved in the `.cache` directory in your working folder.

✅ At the start of each run, the calibration data is checked automatically. If there's an issue, you'll see a prompt in the terminal.
If you are asked to redo the calibration you have to delete the `.cache` directory and start with task 4.1.


### 5. Run Position Control Mode

Once calibrated, run:

```
python test_position_mode.py
```

- Press **'n'** to move to the next position in the predefined list.
- When the list ends, the last position is held.
- Press **'ESC'** to stop the program. Be careful as the torque is disabled and the robot will collapse.


