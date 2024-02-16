# ROS Open Container Initiative Images

[Open Container Initiative](https://opencontainers.org/) images for ROS!

All images are updated once per week (Sunday at midnight GMT).
There are tags matching those for the [Official ROS Images](https://hub.docker.com/_/ros) and [OSRF ROS Images](https://hub.docker.com/r/osrf/ros/tags).

The following ROS distros have images:

* [ROS Rolling](http://docs.ros.org/en/rolling)
* [ROS Iron](http://docs.ros.org/en/iron)
* [ROS Humble](http://docs.ros.org/en/humble)
* [ROS Noetic](https://wiki.ros.org/noetic)

There is a tag for each [variant defined by REP 2001](https://ros.org/reps/rep-2001.html) for the ROS 2 distros.
For [ROS Noetic](https://wiki.ros.org/noetic) which is a ROS 1 distro there is an image for each [metapackage defined by REP 142](https://www.ros.org/reps/rep-0142.html).

This table shows which architectures are supported by each image.

| Image                | amd64 | arm/v7 | arm/v8 | Full Image Name                          |
|----------------------|-------|--------|--------|------------------------------------------|
| Humble ros-core      | ✅     | ❌      | ✅      | ghcr.io/sloretz/ros:humble-ros-core      |
| Humble ros-base      | ✅     | ❌      | ✅      | ghcr.io/sloretz/ros:humble-ros-base      |
| Humble desktop       | ✅     | ❌      | ✅      | ghcr.io/sloretz/ros:humble-desktop       |
| Humble perception    | ✅     | ❌      | ✅      | ghcr.io/sloretz/ros:humble-perception    |
| Humble simulation    | ✅     | ❌      | ✅      | ghcr.io/sloretz/ros:humble-simulation    |
| Humble desktop-full  | ✅     | ❌      | ✅      | ghcr.io/sloretz/ros:humble-desktop-full  |
| Iron ros-core        | ✅     | ❌      | ✅      | ghcr.io/sloretz/ros:iron-ros-core        |
| Iron ros-base        | ✅     | ❌      | ✅      | ghcr.io/sloretz/ros:iron-ros-base        |
| Iron desktop         | ✅     | ❌      | ✅      | ghcr.io/sloretz/ros:iron-desktop         |
| Iron perception      | ✅     | ❌      | ✅      | ghcr.io/sloretz/ros:iron-perception      |
| Iron simulation      | ✅     | ❌      | ✅      | ghcr.io/sloretz/ros:iron-simulation      |
| Iron desktop-full    | ✅     | ❌      | ✅      | ghcr.io/sloretz/ros:iron-desktop-full    |
| Rolling ros-core     | ✅     | ❌      | ✅      | ghcr.io/sloretz/ros:rolling-ros-core     |
| Rolling ros-base     | ✅     | ❌      | ✅      | ghcr.io/sloretz/ros:rolling-ros-base     |
| Rolling desktop      | ✅     | ❌      | ✅      | ghcr.io/sloretz/ros:rolling-desktop      |
| Rolling perception   | ✅     | ❌      | ✅      | ghcr.io/sloretz/ros:rolling-perception   |
| Rolling simulation   | ✅     | ❌      | ✅      | ghcr.io/sloretz/ros:rolling-simulation   |
| Rolling desktop-full | ✅     | ❌      | ✅      | ghcr.io/sloretz/ros:rolling-desktop-full |
| Noetic ros-core      | ✅     | ✅      | ✅      | ghcr.io/sloretz/ros:noetic-ros-core      |
| Noetic ros-base      | ✅     | ✅      | ✅      | ghcr.io/sloretz/ros:noetic-ros-base      |
| Noetic desktop       | ✅     | ✅      | ✅      | ghcr.io/sloretz/ros:noetic-desktop       |
| Noetic perception    | ✅     | ✅      | ✅      | ghcr.io/sloretz/ros:noetic-perception    |
| Noetic simulators    | ✅     | ❌      | ✅      | ghcr.io/sloretz/ros:noetic-simulation    |
| Noetic desktop-full  | ✅     | ❌      | ✅      | ghcr.io/sloretz/ros:noetic-desktop-full  |
| Noetic robot         | ✅     | ✅      | ✅      | ghcr.io/sloretz/ros:noetic-robot         |
| Noetic viz           | ✅     | ✅      | ✅      | ghcr.io/sloretz/ros:noetic-viz           |

# Comparison to osrf/docker_images

This repo is a spiritual fork of [the official OSRF docker images](https://github.com/osrf/docker_images).
The image definitions here were copied and modified from the official ones.
The goal of this repo is to update the images sooner after ROS packages are synced.
This has been [a longstanding issue with the official OSRF Docker images](https://github.com/osrf/docker_images/issues/112) that can't easily be solved due to both [Docker Official Library](https://github.com/docker-library/official-images) policies and how the ROS buildfarm versions packages on different architectures.
