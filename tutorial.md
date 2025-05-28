# Tutorial

1. Check the name of your COM Port: python venv\Lib\site-packages\lbp_2025_robot_control\find_motors_bus_port.py
2. Give every motor a unique ID. Start with the motor at the base and end with the motor at the gripper. To do this unplug all motors but not the one there you want to change the id. While (un)plugging be careful to not interchange the power supply of the first two motors and the others as there is the risk to damage the other motors with a voltage that is too high. With only one motor plugged in run the following script: python venv\Lib\site-packages\lbp_2025_robot_control\configure_motor.py \
  --port /dev/tty.usbmodem58760432961 \
  --model xl330-m288 \
  --baudrate 1000000 \
  --ID 1

Model xl430-w250 for the first two motors and Model xl330-m288 for the rest.

Now you can test the arm with the following script. Here you can select a motor by id with the numeric keys 1-6. After a selection you can turn the motor by holding 'w' and 's'. Press 'esc' if you want to leave the script. Congratulations, your robot is working!

Now you can save a configuration of the motor to do repeatable motions even if you restart the motor. To do so follow the following steps.
