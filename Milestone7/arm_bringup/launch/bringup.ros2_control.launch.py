from launch import LaunchDescription
from launch.substitutions import Command, PathJoinSubstitution

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

    # path buat akses file urdf di package arm_kinematic
    urdf_path = PathJoinSubstitution([FindPackageShare('arm_kinematic'), 'urdf', 'leg.urdf.xacro'])

    xacro_script = Command(['xacro ', urdf_path])

    # node sama kayak launch sebelumnya
    robot_state_publisher = Node(
        package = 'robot_state_publisher',
        executable = 'robot_state_publisher',
        output = 'screen',

        parameters = [{
            'robot_description': ParameterValue(xacro_script, value_type = str)
        }]
    )

    # config controller.yaml dari package yang sama
    controller_config = PathJoinSubstitution([FindPackageShare('arm_bringup'), 'config', 'controller.yaml'])

    # bikin node controller manager yang bakal ngatur gerakan joint-jointnya
    control_node = Node(
        package = 'controller_manager',
        executable = 'ros2_control_node',
        output = 'screen',

        parameters = [controller_config],

        remappings = [
            ('~/robot_description', '/robot_description')
        ]
    )

    joint_trajectory_controller_spawner = Node(
        package = 'controller_manager',
        executable = 'spawner',
        arguments = ['joint_trajectory_controller', '--controller-manager', '/controller_manager']
    )

    joint_state_broadcaster_spawner = Node(
        package = 'controller_manager',
        executable = 'spawner',
        arguments = ['joint_state_broadcaster', '--controller-manager', '/controller_manager']
    )

    rviz_config = PathJoinSubstitution([FindPackageShare('arm_bringup'), 'config', 'leg.rviz'])

    # node rviz2
    rviz2_node = Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
        arguments=['-d', rviz_config]
    )

    # add nodes
    node_list = [
        robot_state_publisher,
        control_node,
        joint_trajectory_controller_spawner,
        joint_state_broadcaster_spawner,
        rviz2_node,
    ]

    return LaunchDescription(node_list)