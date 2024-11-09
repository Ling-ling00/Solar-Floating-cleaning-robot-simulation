from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    launch_description = LaunchDescription()
    package_name = 'solar'

    lidar_read = Node(
        package = package_name,
        executable = 'lidar_read.py',
        name = 'lidar'
    )
    
    robot = Node(
        package = package_name,
        executable = 'robot_control.py',
        name = 'robot'
    )
    
    launch_description.add_action(lidar_read)
    launch_description.add_action(robot)

    return launch_description