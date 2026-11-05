cmake_minimum_required(VERSION 3.20)

project(
    MiniROVFirmware
    VERSION 0.1.0
    DESCRIPTION "Mini ROV Firmware Simulator"
    LANGUAGES CXX
)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_executable(rov_firmware
    firmware/main.cpp
    firmware/src/motor.cpp
    firmware/src/esc.cpp
    firmware/src/controller.cpp
    firmware/src/safety_manager.cpp
)

target_include_directories(rov_firmware
    PRIVATE
        firmware/include
)

if(MSVC)
    target_compile_options(rov_firmware PRIVATE /W4 /WX)
else()
    target_compile_options(rov_firmware PRIVATE -Wall -Wextra -Wpedantic -Werror)
endif()