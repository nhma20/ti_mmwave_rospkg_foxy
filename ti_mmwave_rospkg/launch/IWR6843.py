import os
from launch import LaunchDescription, conditions
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution

def generate_launch_description():

    # Declare the launch argument
    cfg_file_arg = DeclareLaunchArgument(
        'cfg_file',
        default_value='6843ISK_Tracking.cfg'
    )

    command_port_arg = DeclareLaunchArgument(
        'command_port',
        default_value='/dev/ttyUSB0'
    )

    data_port_arg = DeclareLaunchArgument(
        'data_port',
        default_value='/dev/ttyUSB1'
    )

    rviz_arg = DeclareLaunchArgument(
        'rviz',
        default_value='true',
        description='Enable RViz'
    )

    # Use the launch argument in the condition for adding the RViz node
    rviz_enabled = LaunchConfiguration('rviz')

    # Enter Path and Name Here
    my_package_dir = get_package_share_directory('ti_mmwave_rospkg')
    cfg_file = LaunchConfiguration("cfg_file")
    mmwavecli_cfg_path = PathJoinSubstitution([my_package_dir, 'cfg', cfg_file])

    device = "6843"
    name = "/mmWaveCLI"
    command_port = LaunchConfiguration("command_port")
    command_rate = "115200"
    data_port = LaunchConfiguration("data_port")
    data_rate = "921600"

    ConfigParameters = os.path.join(
        my_package_dir,
        'config',
        'global_params.yaml',
        'launch/*.rviz'
    )
    global_param_node = Node(
        package='ti_mmwave_rospkg',
        executable='ConfigParameterServer',
        name='ConfigParameterServer',
        parameters=[ConfigParameters]
    )

    mmWaveCommSrv = Node(
        package="ti_mmwave_rospkg",
        executable="mmWaveCommSrv",
        name="mmWaveCommSrv",
        output="screen",
        emulate_tty=True,
        parameters=[
            {"command_port": command_port},
            {"command_rate": command_rate},
        ]
    )

    mmWaveQuickConfig = Node(
        package="ti_mmwave_rospkg",
        executable="mmWaveQuickConfig",
        name="mmWaveQuickConfig",
        output="screen",
        emulate_tty=True,
        parameters=[
            {"mmwavecli_cfg": mmwavecli_cfg_path}
        ]
    )

    ParameterParser = Node(
        package="ti_mmwave_rospkg",
        executable="ParameterParser",
        name="ParameterParser",
        output="screen",
        emulate_tty=True,
        parameters=[
            {"device_name": device},
            {"mmwavecli_cfg": mmwavecli_cfg_path}
        ]
    )

    DataHandlerClass = Node(
        package="ti_mmwave_rospkg",
        executable="DataHandlerClass",
        name="DataHandlerClass",
        output="screen",
        emulate_tty=True,
        parameters=[
            {"data_port": data_port},
            {"data_rate": data_rate},
            {"max_allowed_elevation_angle_deg": 90},
            {"max_allowed_azimuth_angle_deg": 90},
            {"frame_id": "ti_mmwave_0"}
        ]

    )

    Rviz2 = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', os.path.join(my_package_dir, 'launch', 'rviz.rviz')],
        condition=conditions.IfCondition(rviz_enabled)  # only launch RViz if the argument is true
    )

    ld = LaunchDescription()
    ld.add_action(cfg_file_arg)
    ld.add_action(command_port_arg)
    ld.add_action(data_port_arg)
    ld.add_action(rviz_arg)
    ld.add_action(global_param_node)
    ld.add_action(mmWaveCommSrv)
    ld.add_action(mmWaveQuickConfig)
    ld.add_action(ParameterParser)
    ld.add_action(DataHandlerClass)
    ld.add_action(Rviz2)

    return ld
