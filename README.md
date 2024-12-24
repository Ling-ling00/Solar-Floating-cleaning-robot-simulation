# **Introduction**
This project is inspired by an ongoing real-world research initiative involving autonomous robots designed to navigate solar floating platforms installed on buoyant structures in the middle of Sirindhorn Dam. The integration of autonomous robotic systems aims to enhance their maintenance, monitoring, and operational efficiency

![alt text](image.png)

In this project, we recreate this scenario in a simulated environment using ROS2 and Gazebo. The simulation is designed to replicate real-world dynamics as accurately as possible, incorporating realistic physics, including the buoyancy effects of the floating buoys. The robot is equipped with virtual sensors such as a 2D LiDAR and an IMU. These sensors provide feedback on the robot's movement and enable precise control for navigation and compensation of the robot movement within the floating solar platform environment
 
![alt text](image-1.png)

The objective of this simulation is to create a virtual testing ground for developing and refining algorithms for autonomous navigation, path planning, and environmental interaction. By closely mirroring the conditions of the Sirindhorn Dam, this project provides a valuable platform for testing and improving the performance of the robotic system before real-world deployment.

 ![alt text](image-2.png)

# **Set up and installation**
Before starting, ensure you have the following installed: <br>
    •	Operating System: Ubuntu 22.04 (recommended)<br>
    •	ROS 2: Humble or compatible version<br>
    •	Gazebo: Fortress or compatible version<br>
    •	Python: 3.10+<br>
    •	colcon: For building the ROS 2 workspace<br><br>
Install ROS 2 and Gazebo by following their official installation guides:<br>
    •	[ROS 2 Installation Guide](https://docs.ros.org/en/humble/Installation.html)<br>
    •	[Gazebo Installation Guide](https://classic.gazebosim.org/tutorials?tut=install_ubuntu)<br>
<br>

Then installed all the dependency of this project by this command 

```
sudo apt install ros-humble-gazebo-ros-pkgs
```
```
sudo apt install ros-humble-robot-state-publisher
```
```
sudo apt install ros-humble-controller-manager
```
```
sudo apt install ros-humble-gazebo-ros2-control
```
```
sudo apt-get install ros-humble-imu-tools
```

Then clone the library repository that we going to use in the desire directory

```
cd ~ | git clone https://github.com/Ling-ling00/Solar-Floating-cleaning-robot-simulation.git -b floating Lib_Solar-Floating-cleaning-robot-simulation
```
then build the workspace with this command  
```
cd Lib_Solar-Floating-cleaning-robot-simulation 
mkdir build
cd build
cmake ..
make
sudo make install
```
Then installed project using this command 
```
cd ~ | git clone https://github.com/Ling-ling00/Solar-Floating-cleaning-robot-simulation.git
```
then build the workspace with this command  
```
cd Solar-Floating-cleaning-robot-simulation
colcon build
```
Then source the installation with this command 
```
source install/setup.bash
cd src/lidar_gazebo
source gazebo.sh
```
Then test the installation with this command 
```
gazebo worlds/freebuoyancy_demo.world -u
```
If the installation successful, The world that replicate the Solar-floating will appear with realistic buoyancy in each floating buoy

![alt text](image-3.png)
 
# **System architect**

![alt text](image-4.png)

## **Robot State Publisher**
-	Publishes the /tf topic by taking the robot.xacro URDF model and computing the transforms between the robot’s links.
## **World**
-	Simulates a floating solar cell panel in Gazebo by combining SDF models with the FreeBuoyancy plugin.
## **Gazebo Simulation**
-	Uses Gazebo as the physics engine to visualize and simulate buoyancy effects and the robot’s movements within the world.
## **Gazebo Plugins**
-	**Sensor Plugins**
    -	Publish data from simulated IMU and LiDAR sensors via the topic imu/out and lidar/out.
-	**ROS 2 Control Plugin**
    -	Apply control of robot wheels’ velocity via /velocity_controllers/commands topic using ROS 2 controllers.
-	**Freebuoyancy Plugin**
    -	Simulates buoyancy effects in underwater or floating scenarios.
## **Lidar_read_node**
-	Subscribes to the /lidar/out topic and calculates the error in rotation and position offset. And uses a P-controller to correct the robot’s position and rotation accordingly by publish /velocity_controllers/commands topic.
## **RVIZ**
-	Visualizes the robot’s movement, the IMU data in the robot’s base frame, and the LiDAR data in real-time.

# **Technical detail**
## **Robot**
-	In this project we simulate robot mass and inertia approximately to real robot by follow the properties in CAD
Robot body mass and inertia

  ![alt text](image-5.png)

  ![alt text](image-6.png)

Robot wheel mass

 ![alt text](image-7.png)

## **Sensor**
-	To visualize the position and rotation of robot we visualize 2 sesors
-	**LiDAR** position of LiDAR is at the top of robot and look down to detect the edge of solar cell panel.
Data that LiDAR can read visualize in RVIZ

 ![alt text](image-8.png)

Position of robot in simulation 

![alt text](image-9.png)

-	**IMU** position of imu is at the base of robot to calculate rotation around Y-axis for report that is robot in the hole between floating.
Data that IMU can read visualize in RVIZ

![alt text](image-10.png)
  
Position of robot in simulation

 ![alt text](image-11.png)
## **World**
-	In the world file will be include 3 SDF file 
 
![alt text](image-12.png)

## test2 or floating buoy and Solar panel 

This file will consist of floating buoy and Solar panel in sdf form 

 ![alt text](image-13.png)
 
 with the plugin freebuoyancy_gazebo from libraly libfreebuoyancy_gazebo 
 
![alt text](image-14.png)

Visualize of test2.sdf 

 ![alt text](image-15.png)

## Path1 and path2 
Is the path ways for the robot movement that will be place above the floating buoy.In this sdf file will not include the buoyancy plugin 

 ![alt text](image-16.png)


Visualize of path1 and path2 that are on top of the  test2.sdf 

 ![alt text](image-17.png)

# **Demo & How to use** 
## **World launch**
To launch the empty world use this command 
```
ros2 launch lidar_gazebo test_world.launch.py
```
The result of the command will open the gazebo world with only the solar panel and floating buoy 

 ![alt text](image-18.png)

## **World with robot launch**
To launch solar panel and floating buoy with robot run this command
```
ros2 launch lidar_gazebo gazebo.launch.py
```

 ![alt text](image-19.png)
 
## **Controller**
To control robot with controller
```
ros2 run solar lidar_read_sim.py
```
To control robot with fixed speed (v(l) is left front and back wheel speed in forward direction and v(r) is right front and back wheel speed in forward direction)
```
ros2 topic pub /velocity_controllers/commands std_msgs/msg/Float64MultiArray "layout:
  dim: []
  data_offset: 0
data: [-v(l), -v(l), v(r), v(r)]"
``` 

# **Demo & How to use** 
-	วิธี run world เปล่า เล่น buoyancy 
-	Run เต็ม
# **Validation**
-	Video + 3d graph เทียบารเคลื่อนที่ 
# **Future plan**


# **Contributor**


