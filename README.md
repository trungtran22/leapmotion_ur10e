# Teleop control - Leap Motion - Robot Arm
Controlling Ur10e Robot Arm via Leap Motion Controller - Teleop Control

**Clone universal_robot package version 1.2.7:**
```
cd ~/catkin_ws/src
git clone -b 1.2.7 https://github.com/ros-industrial/universal_robot
rosdep install -y --from-paths . --ignore-src --rosdistro $ROS_DISTRO
```
**Clone leap_motion ROS package:**

```
# 64-bit operating system
export PYTHONPATH=$PYTHONPATH:$HOME/LeapSDK/lib:$HOME/LeapSDK/lib/x64

# 32-bit operating system
export PYTHONPATH=$PYTHONPATH:$HOME/LeapSDK/lib:$HOME/LeapSDK/lib/x86

cd ~/catkin_ws/src
git clone https://github.com/ros-drivers/leap_motion.git
rosdep install -y --from-paths . --ignore-src --rosdistro $ROS_DISTRO
cd ~/catkin_ws
catkin build
```

This project will use package `moveit_servo` for realtime servoing the UR10e. Leapmotion `hand.palm_position`, `hand.pitch`, `hand.yaw` and `hand.roll` will be transmitted to the robot arm as geometry_msgs/TwistStamped (`linear` and `angular`)

**Implementation (Gazebo):**

```
#launch ur10e
roslaunch ur_e_gazebo ur10e.launch
roslaunch ur10_e_moveit_config ur10e_moveit_planning_execution.launch sim:=true
roslaunch ur10_e_moveit_config moveit_rviz.launch config:=true

#launch leap_motion
sudo leapd
LeapControlPanel --showsettings
Visualizer

#change controllers to JointGroupPositionController or JointGroupVelocityController
rosservice call /controller_manager/switch_controller "start_controllers: ['joint_group_position_controller']
stop_controllers: ['arm_controller']
strictness: 0
start_asap: false
timeout: 0.0"

#launch leap control
roslaunch leap_robot_arm leap_teleop_ur.launch

#publish fake signal
rostopic pub -r 100 -s /servo_server/delta_twist_cmds geometry_msgs/TwistStamped "header: auto
twist:
  linear:
    x: 0
    y: 0
    z: 0.1
  angular:
    x: 0
    y: 0
    z: 0"
```
**Demo Video:**
https://youtu.be/j1su4HBF2Ig?feature=shared
