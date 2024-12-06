cmake_minimum_required(VERSION 3.5)
project(lidar_gazebo)

# Default to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

################ FIND DEPENDENCIES #################
find_package(ament_cmake REQUIRED)       # cpp (optional)
find_package(rclcpp REQUIRED)           # cpp (optional)
find_package(ament_cmake_python REQUIRED) # python (optional)
find_package(rclpy REQUIRED)            # python (optional)
find_package(gazebo REQUIRED)           # gazebo

include_directories(
  ${GAZEBO_INCLUDE_DIRS}
  include
)

link_directories(${GAZEBO_LIBRARY_DIRS})

#####################################################

# Install Python Module
ament_python_install_package(${PROJECT_NAME})

# Install Python executables
install(PROGRAMS
  scripts/dummy_script.py
  DESTINATION lib/${PROJECT_NAME}
)

# Create Cpp executable
add_executable(cpp_node_test src/cpp_node.cpp)
ament_target_dependencies(cpp_node_test rclcpp)

# Install Cpp executables
install(TARGETS
  cpp_node_test
  DESTINATION lib/${PROJECT_NAME}
)

# Create Gazebo plugin library
add_library(freebuoyancy_gazebo SHARED
  src/freebuoyancy.cpp
  src/freebuoyancy.h
)

target_link_libraries(freebuoyancy_gazebo ${GAZEBO_LIBRARIES})

# Install Gazebo plugin
install(TARGETS freebuoyancy_gazebo
  DESTINATION lib/${PROJECT_NAME}
)

# Install headers
install(DIRECTORY
  src/
  DESTINATION include/${PROJECT_NAME}
  FILES_MATCHING PATTERN "*.h"
)

# Install additional files (e.g., launch files)
install(DIRECTORY
  launch
  worlds
  DESTINATION share/${PROJECT_NAME})

ament_package()
