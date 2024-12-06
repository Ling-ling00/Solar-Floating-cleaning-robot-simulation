#!/usr/bin/env python3

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
import os

def generate_launch_description():
    # Path to the world file
    world_file_name = "freebuoyancy_demo.world"
    world_file_path = os.path.join(
        get_package_share_directory("lidar_gazebo"),
        "worlds",
        world_file_name
    )

    # Ensure the world file exists
    if not os.path.exists(world_file_path):
        raise FileNotFoundError(f"World file '{world_file_path}' does not exist.")

    # Launch Gazebo with the specific world
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare("gazebo_ros"),
                "launch",
                "gazebo.launch.py"
            ])
        ),
        launch_arguments={
            "world": world_file_path
        }.items()
    )

    # Return the launch description
    return LaunchDescription([gazebo])
