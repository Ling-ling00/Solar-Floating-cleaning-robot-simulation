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
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
import xacro  

def generate_launch_description():
    package_name = "lidar_description"
    rviz_file_name = "gazebo.rviz"
    rviz_file_path = os.path.join(
        get_package_share_directory(package_name),
        'rviz',
        rviz_file_name
    )
    
    # Path to the world file
    # world_file_name = "freebuoyancy_demo.world"
    world_file_name = "freebuoyancy_demo.world"
    world_file_path = os.path.join(
        get_package_share_directory("lidar_gazebo"),
        'worlds',
        world_file_name
    )

    # Include the robot description launch
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(
                    get_package_share_directory(package_name),
                    "launch",
                    "robot2.launch.py"
                )
            ]
        ),
        launch_arguments={"use_sim_time": "true"}.items()
    )

    # Include the robot description launch
    path = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(
                    get_package_share_directory(package_name),
                    "launch",
                    "path.launch.py"
                )
            ]
        ),
        launch_arguments={"use_sim_time": "true"}.items()
    )

    # Launch Gazebo with the specific world
    gazebo2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(
                    get_package_share_directory("gazebo_ros"),
                    "launch",
                    "gazebo.launch.py"
                )
            ]
        )
        # launch_arguments={"gz_args": world_file_path}.items()
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
    

    spawn_entity = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=[
            "-topic", "/robot/robot_description",
            "-entity", "robot",
            "-x", "-10.0",
            "-y", "0.0",
            "-z", "0.2"
        ],
        output="screen"
    )

    spawn_entity2 = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=[
            "-topic", "/walk_path/robot_description",
            "-entity", "walk_path",
            "-x", "0.0",
            "-y", "0.8",
            "-z", "0.0"
        ],
        output="screen"
    )

    spawn_entity3 = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=[
            "-topic", "/walk_path/robot_description",
            "-entity", "walk_path2",
            "-x", "0.0",
            "-y", "-0.8",
            "-z", "0.0"
        ],
        output="screen"
    )


    # Launch RViz
    rviz = Node(
        package="rviz2",
        executable="rviz2",
        arguments=["-d", rviz_file_path],
        output="screen"
    )

    # Controllers
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
    )

    robot_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["velocity_controllers", "--controller-manager", "/controller_manager"],
    )

    # Launch!
    return LaunchDescription(
        [
            gazebo,
            spawn_entity,
            # spawn_entity2,
            # spawn_entity3,
            rsp,
            path,
            rviz,
            joint_state_broadcaster_spawner,
            robot_controller_spawner,
            
        ]
    )
