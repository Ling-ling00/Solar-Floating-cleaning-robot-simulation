#!/usr/bin/env python3

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro  
def generate_launch_description():
    package_name = "lidar_description"
    rviz_file_name = "gazebo.rviz"
    rviz_file_path = os.path.join(
        get_package_share_directory(package_name),
        'rviz',
        rviz_file_name
    )

    # rsp = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(
    #         [
    #             os.path.join(
    #                 get_package_share_directory(package_name),
    #                 "launch",
    #                 "robot.launch.py"
    #             )
    #         ]
    #     ),
    #     launch_arguments={"use_sim_time":"true"}.items()
    # )

    # solar = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(
    #         [
    #             os.path.join(
    #                 get_package_share_directory(package_name),
    #                 "launch",
    #                 "solar.launch.py"
    #             )
    #         ]
    #     ),
    #     launch_arguments={"use_sim_time":"true"}.items()
    # )

    buoyon = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(
                    get_package_share_directory(package_name),
                    "launch",
                    "buoyon.launch.py"
                )
            ]
        ),
        launch_arguments={"use_sim_time":"true"}.items()
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(
                    get_package_share_directory("gazebo_ros"),
                    "launch",
                    "gazebo.launch.py"
                )
            ]
        )
    )
    
    # spawn_entity = Node(
    #     package="gazebo_ros",
    #     executable="spawn_entity.py",
    #     arguments=[
    #         "-topic", "/robot/robot_description",
    #         "-entity", "robot",
    #         "-x", "0.0",
    #         "-y", "0.0",
    #         "-z", "0.0"],
    #     output = "screen"
    # )

    spawn_entity2 = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=[
            "-topic", "/buoyon/robot_description",
            "-entity", "buoyon",
            "-x", "0.0",
            "-y", "0.0",
            "-z", "5.0"],
        output = "screen"
    )

    # rviz = Node(
    #     package="rviz2",
    #     executable="rviz2",
    #     arguments=[
    #         "-d", rviz_file_path
    #     ],
    #     output = "screen"
    # )

    # joint_state_broadcaster_spawner = Node(
    #     package="controller_manager",
    #     executable="spawner",
    #     arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
    # )

    # robot_controller_spawner = Node(
    #     package="controller_manager",
    #     executable="spawner",
    #     arguments=["velocity_controllers", "--controller-manager", "/controller_manager"],
    # )

    # Launch!
    return LaunchDescription(
        [   
            gazebo,
            # spawn_entity,
            spawn_entity2,
            # rsp,
            # solar,
            # rviz,
            # joint_state_broadcaster_spawner,
            # robot_controller_spawner,
            buoyon
        ]
    )