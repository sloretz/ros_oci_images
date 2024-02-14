#!/bin/bash
set -eu -o pipefail

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

source "${SCRIPT_DIR}/build_image_functions.bash"

function build_ros1_images() {
    rosdistro=$1
    baseimage=$2

    ros1_build_ros_core     $rosdistro   $baseimage                            ros_oci_images:$rosdistro-ros-core
    ros1_build_ros_base     $rosdistro   ros_oci_images:$rosdistro-ros-core    ros_oci_images:$rosdistro-ros-base
    build_desktop           $rosdistro   ros_oci_images:$rosdistro-ros-base    ros_oci_images:$rosdistro-desktop
    ros1_build_perception   $rosdistro   ros_oci_images:$rosdistro-ros-base    ros_oci_images:$rosdistro-perception
    ros1_build_simulators   $rosdistro   ros_oci_images:$rosdistro-ros-base    ros_oci_images:$rosdistro-simulators
    ros1_build_viz          $rosdistro   ros_oci_images:$rosdistro-ros-base    ros_oci_images:$rosdistro-viz
    ros1_build_robot        $rosdistro   ros_oci_images:$rosdistro-ros-base    ros_oci_images:$rosdistro-robot
    build_desktop_full      $rosdistro   ros_oci_images:$rosdistro-desktop     ros_oci_images:$rosdistro-desktop-full
}

function build_ros2_images() {
    rosdistro=$1
    baseimage=$2

    ros2_build_ros_core     $rosdistro   $baseimage                            ros_oci_images:$rosdistro-ros-core
    ros2_build_ros_base     $rosdistro   ros_oci_images:$rosdistro-ros-core    ros_oci_images:$rosdistro-ros-base
    build_desktop           $rosdistro   ros_oci_images:$rosdistro-ros-base    ros_oci_images:$rosdistro-desktop
    ros2_build_perception   $rosdistro   ros_oci_images:$rosdistro-ros-base    ros_oci_images:$rosdistro-perception
    ros2_build_simulation   $rosdistro   ros_oci_images:$rosdistro-ros-base    ros_oci_images:$rosdistro-simulation
    build_desktop_full      $rosdistro   ros_oci_images:$rosdistro-desktop     ros_oci_images:$rosdistro-desktop-full
}

function print_usage() {
    echo "Usage: build_ros_images.bash ROS_DISTRO"
    echo
    echo "Supported values for ROS_DISTRO are: noetic, humble, iron, rolling"
}

if [ "$#" -ne 1 ]; then
    print_usage
    exit 1
fi


case $1 in
    noetic)
        build_ros1_images noetic ubuntu:focal
        ;;
    humble)
        build_ros2_images humble ubuntu:jammy
        ;;
    iron)
        build_ros2_images iron ubuntu:jammy
        ;;
    rolling)
        build_ros2_images rolling ubuntu:jammy
        ;;
    *)
        print_usage
        exit 1
        ;;
esac