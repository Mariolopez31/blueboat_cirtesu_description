import os
import shlex
import subprocess

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def launch_setup(context, *args, **kwargs):
    robot_description_package = LaunchConfiguration(
        "robot_description_package"
    ).perform(context).strip()
    if not robot_description_package:
        raise RuntimeError(
            "Launch argument 'robot_description_package' is required and cannot be empty."
        )

    package_share = get_package_share_directory(robot_description_package)
    xacro_relative_path = LaunchConfiguration("xacro_file").perform(context).strip()
    xacro_file = os.path.join(package_share, xacro_relative_path)
    xacro_arguments = LaunchConfiguration("xacro_arguments").perform(context).strip()

    command = ["xacro", xacro_file]
    if xacro_arguments:
        command.extend(shlex.split(xacro_arguments))

    robot_description = subprocess.check_output(command, text=True)

    return [
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            name="robot_state_publisher",
            parameters=[{"robot_description": robot_description}],
            output="screen",
        )
    ]


def generate_launch_description():
    return LaunchDescription(
        [
            DeclareLaunchArgument("robot_description_package"),
            DeclareLaunchArgument("xacro_file"),
            DeclareLaunchArgument("xacro_arguments", default_value=""),
            OpaqueFunction(function=launch_setup),
        ]
    )
