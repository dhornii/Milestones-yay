import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/tsaqip/ros2_ws/src/Arm_Kinematics/install/Arm_Kinematics'
