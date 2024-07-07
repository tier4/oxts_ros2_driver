import os
import yaml
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def load_params(context):
    # Get the driver_param_path argument value
    driver_param_path = LaunchConfiguration('driver_param_path').perform(context)
    ins_param_path = LaunchConfiguration('ins_param_path').perform(context)

    # Load the parameters from the YAML file
    with open(driver_param_path, 'r') as f:
        driver_params = yaml.safe_load(f)["oxts_driver"]["ros__parameters"]
    with open(ins_param_path, 'r') as f:
        ins_params = yaml.safe_load(f)["oxts_ins"]["ros__parameters"]

    # Extract individual parameters from the loaded parameters
    use_sim_time = driver_params.pop("use_sim_time", False)
    wait_for_init = driver_params.pop("wait_for_init", False)
    print(f"wait_for_init: {wait_for_init}")
    ncom_file = driver_params.pop("ncom_file", "")
    unit_ip = driver_params.pop("unit_ip","0.0.0.0")
    unit_port = driver_params.pop("unit_port", 3000)
    ncom_rate = driver_params.pop("ncom_rate", 100)
    timestamp_mode = driver_params.pop("timestamp_mode", 1)
    
    frame_id = ins_params.pop("frame_id", "base_link")
    lrf_source = ins_params.pop("lrf_source", "none")

    # Create the Node action with the loaded parameters
    oxts_driver_node = Node(
        package="oxts_driver",
        executable="oxts_driver",
        name="oxts_driver",
        output="screen",
        parameters=[
            driver_params,
            {"use_sim_time": use_sim_time},
            {"wait_for_init": wait_for_init},
            {"ncom": ncom_file},
            {"unit_ip": unit_ip},
            {"unit_port": unit_port},
            {"ncom_rate": ncom_rate},
            {"timestamp_mode": timestamp_mode},
        ],
    )

    oxts_ins_node = Node(
        package="oxts_ins",
        executable="oxts_ins",
        name="oxts_ins",
        output="screen",
        parameters=[
            ins_params,
            {"use_sim_time": use_sim_time},
            {"frame_id": frame_id},
            {"lrf_source": lrf_source},
        ],
    )


    return [oxts_driver_node, oxts_ins_node]

def generate_launch_description():
    # Get the package share directory
    driver_dir = get_package_share_directory("oxts_driver")
    ins_dir = get_package_share_directory("oxts_ins")

    # Declare the driver_param_path argument
    driver_param_path_arg = DeclareLaunchArgument(
        'driver_param_path',
        default_value=os.path.join(driver_dir, "config", "default.yaml"),
        description='Path to the OXTS driver YAML file'
    )
    ins_param_path_arg = DeclareLaunchArgument(
        'ins_param_path',
        default_value=os.path.join(ins_dir, "config", "default.yaml"),
        description='Path to the OXTS ins YAML file'
    )
    return LaunchDescription([
        driver_param_path_arg,
        ins_param_path_arg,
        OpaqueFunction(function=load_params)
    ])
