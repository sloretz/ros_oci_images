#!/bin/bash
set -eu -o pipefail

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

source "${SCRIPT_DIR}/build_image_functions.bash"

architectures="${ARCHITECTURES:-amd64,arm32v7,arm64v8}"

function multiarch_build() {
    # Create a manifest for the multiarch image.
    buildah manifest create $imagename

    while IFS=',' read -ra ADDR; do
        for arch in "${ADDR[@]}"; do
            echo $arch
        done
    done <<< "$architectures"
}

function build_ros1_images() {
    rosdistro=$1
    baseimage=$2
    imagename=$3

    ros1_build_ros_core     $rosdistro   $baseimage                        $imagename:$rosdistro-ros-core
    ros1_build_ros_base     $rosdistro   $imagename:$rosdistro-ros-core    $imagename:$rosdistro-ros-base
    build_desktop           $rosdistro   $imagename:$rosdistro-ros-base    $imagename:$rosdistro-desktop
    build_perception        $rosdistro   $imagename:$rosdistro-ros-base    $imagename:$rosdistro-perception
    ros1_build_simulators   $rosdistro   $imagename:$rosdistro-ros-base    $imagename:$rosdistro-simulators
    ros1_build_viz          $rosdistro   $imagename:$rosdistro-ros-base    $imagename:$rosdistro-viz
    ros1_build_robot        $rosdistro   $imagename:$rosdistro-ros-base    $imagename:$rosdistro-robot
    build_desktop_full      $rosdistro   $imagename:$rosdistro-desktop     $imagename:$rosdistro-desktop-full
}

function build_ros2_images() {
    rosdistro=$1
    baseimage=$2
    imagename=$3

    ros2_build_ros_core     $rosdistro   $baseimage                        $imagename:$rosdistro-ros-core
    ros2_build_ros_base     $rosdistro   $imagename:$rosdistro-ros-core    $imagename:$rosdistro-ros-base
    build_desktop           $rosdistro   $imagename:$rosdistro-ros-base    $imagename:$rosdistro-desktop
    build_perception        $rosdistro   $imagename:$rosdistro-ros-base    $imagename:$rosdistro-perception
    ros2_build_simulation   $rosdistro   $imagename:$rosdistro-ros-base    $imagename:$rosdistro-simulation
    build_desktop_full      $rosdistro   $imagename:$rosdistro-desktop     $imagename:$rosdistro-desktop-full
}

function print_usage() {
    echo "Usage: build_ros_images.bash ROS_DISTRO IMAGE_NAME"
    echo
    echo "Supported values for ROS_DISTRO are: noetic, humble, iron, rolling"
}

if [ "$#" -ne 2 ]; then
    print_usage
    exit 1
fi

rosdistro=$1
imagename=$2

case $rosdistro in
    noetic)
        build_ros1_images noetic ubuntu:focal $imagename
        ;;
    humble)
        build_ros2_images humble ubuntu:jammy $imagename
        ;;
    iron)
        build_ros2_images iron ubuntu:jammy $imagename
        ;;
    rolling)
        build_ros2_images rolling ubuntu:jammy $imagename
        ;;
    *)
        print_usage
        multiarch_build
        exit 1
        ;;
esac