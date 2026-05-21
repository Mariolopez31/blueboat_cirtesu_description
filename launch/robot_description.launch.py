import os
import shlex
import subprocess

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def launch_setup(context, *args, **kwargs):
    package_share = get_package_share_directory("blueboat_cirtesu_description")
    xacro_relative_path = LaunchConfiguration("xacro_file").perform(context)
    if not xacro_relative_path:
        xacro_relative_path = os.path.join("urdf", "blueboat.xacro")

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
            DeclareLaunchArgument("xacro_file", default_value=os.path.join("urdf", "blueboat.xacro")),
            DeclareLaunchArgument("xacro_arguments", default_value=""),
            OpaqueFunction(function=launch_setup),
        ]
    )
