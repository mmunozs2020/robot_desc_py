import os
from os.path import join

from ament_index_python.packages import get_package_share_directory

from launch_ros.parameter_descriptions import ParameterValue
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess
from launch.conditions import IfCondition
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch.substitutions import PythonExpression
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit

def generate_launch_description():

    # world_package = get_package_share_directory('robot_desc_pyy')
    model_arg = DeclareLaunchArgument(name='model', description='Absolute path to robot urdf file')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    use_sim_time = LaunchConfiguration('use_sim_time')
    package_name = 'robot_desc_py'
    pkg_share = FindPackageShare(package=package_name).find(package_name)
    pkg_gazebo_ros = FindPackageShare(package='gazebo_ros').find('gazebo_ros')

    world_file_path = '/home/msdelta/modsimspace/src/robot_desc_py/worlds/sand.world'
    world = LaunchConfiguration('world')

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        name='use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true'
    )

    declare_world_cmd = DeclareLaunchArgument(
        name='world',
        default_value=world_file_path,
        description='Full path to the world model file to load'
    )

    robot_name_in_model = 'rover'

    # Get URDF via xacro

    urdf_file_name = 'rover.urdf.xacro'
    urdf = os.path.join(
        get_package_share_directory('robot_desc_py'),
        'urdf',
        urdf_file_name
    )
    with open(urdf, 'r') as infp:
        robot_desc = infp.read()

    robot_description = {"robot_description": robot_desc}

    # rviz2
    rviz2 = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='log',
        parameters=[{'use_sim_time': use_sim_time}],
    )

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'use_sim_time': use_sim_time, 'robot_description': robot_desc}]
    )

    start_joint_state_publisher_cmd = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        parameters=[{'use_sim_time': use_sim_time}],
        name='joint_state_publisher',
    )

    # Spawn the robot
    spawn = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=["-topic", "/robot_description",
                   "-entity", robot_name_in_model,
                   "-x", '0.0',
                   "-y", '0.0',
                   "-z", '1.0',
                   "-Y", '0.0'],
        output='screen'
    )

    gazebo = ExecuteProcess(
        cmd=['gazebo', '--verbose', world_file_path, '-s', 'libgazebo_ros_factory.so',
             '-s', 'libgazebo_ros_init.so'],
        output='screen'
    )

    return LaunchDescription([
        # DeclareLaunchArgument('world', default_value=[PythonExpression(['"',join(world_package, 'worlds'),'" + "/floor.world"']),'']),
        # DeclareLaunchArgument('gui', default_value='true'),
        # DeclareLaunchArgument('verbose', default_value='true'),
        declare_use_sim_time_cmd,
        declare_world_cmd,
        gazebo,
        spawn,
        start_joint_state_publisher_cmd,
        robot_state_publisher_node,
        # rviz2
    ])

