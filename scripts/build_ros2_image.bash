#!/bin/bash
set -eux -o pipefail

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

source "${SCRIPT_DIR}/build_image_functions.bash"

function build_all_images() {
    rosdistro=$1

    ros2_build_ros_core     $rosdistro   ubuntu:jammy                          ros_oci_images:$rosdistro-ros-core
    ros2_build_ros_base     $rosdistro   ros_oci_images:$rosdistro-ros-core    ros_oci_images:$rosdistro-ros-base
    build_desktop           $rosdistro   ros_oci_images:$rosdistro-ros-base    ros_oci_images:$rosdistro-desktop
    ros2_build_perception   $rosdistro   ros_oci_images:$rosdistro-ros-base    ros_oci_images:$rosdistro-perception
    ros2_build_simulation   $rosdistro   ros_oci_images:$rosdistro-ros-base    ros_oci_images:$rosdistro-simulation
    build_desktop_full      $rosdistro   ros_oci_images:$rosdistro-desktop     ros_oci_images:$rosdistro-desktop-full
}

# TODO Arguments here
build_all_images humble