# TI mmWave ROS2 Package (adapted for ROS2 Foxy)

Adapted from: https://git.ti.com/cgit/mmwave_radar/mmwave_ti_ros/tree/ros2_driver


### Install & Run

1. 
```
git clone https://github.com/nhma20/ti_mmwave_rospkg_foxy.git
```
2. Move directories `serial-ros2-master`, `ti_mmwave_rospkg`, and `ti_mmwave_rospkg_msgs` into the `src` folder of your ROS2 workspace.
3. Source your ROS2 underlay
```
source /opt/ros/foxy/setup.bash
```
4. build workspace normally, or selectively with `--packages-up-to` (`--packages-select` does not work).
```
colcon build --packages-up-to ti_mmwave_rospkg
```
5. Source your ROS2 overlay
```
source install/setup.sh
```
6. Plug in TI mmWave radar device and launch
```
ros2 launch ti_mmwave_rospkg 6843AOP_custom2.py
```

<img src="https://github.com/user-attachments/assets/16f08e17-f457-4f56-81ee-113271efb708" width="500">


### Documentation

See `ti_mmwave_rospkg` readme.
