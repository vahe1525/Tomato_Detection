cmake_minimum_required(VERSION 3.10)
project(TomatoDetection)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Find OpenCV package
find_package(OpenCV REQUIRED)

# Find Python package
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)

# Include directories
include_directories(${OpenCV_INCLUDE_DIRS})
include_directories(${Python3_INCLUDE_DIRS})

# Add the executable
add_executable(detect
    main.cpp
    PYCaller.hpp
    PYListConverter.hpp
    Position.hpp
)

# Link libraries
target_link_libraries(detect ${OpenCV_LIBS} ${Python3_LIBRARIES} python3.11)

# Specify the output directory for the executable
set_target_properties(detect PROPERTIES RUNTIME_OUTPUT_DIRECTORY ..)

