# ROS Open Container Initiative Images

[https://opencontainers.org/](Open Container Initiative) images for ROS!

All images are updated once per week (Sunday at midnight GMT).
There are tags matching those for the [Official ROS Images](https://hub.docker.com/_/ros) and [OSRF ROS Images](https://hub.docker.com/r/osrf/ros/tags).
These images are drop-in replacements.

The following ROS 2 distros have images:

* [Rolling](http://docs.ros.org/en/rolling)
* [Iron](http://docs.ros.org/en/iron)
* [Humble](http://docs.ros.org/en/humble)

Each ROS 2 distro has a tag for each [variant defined by REP 2001](https://ros.org/reps/rep-2001.html).

* `DISTRO-simulation`
* `DISTRO-desktop-full`
* `DISTRO-desktop`
* `DISTRO-perception`
* `DISTRO-ros-base`
* `DISTRO-ros-core`

Thre are also tags for the ROS 1 distro [ROS Noetic](https://wiki.ros.org/noetic) for each [metapackage defined by REP 142](https://www.ros.org/reps/rep-0142.html).

* `noetic-ros-core`
* `noetic-ros-base`
* `noetic-robot`
* `noetic-perception`
* `noetic-simulators`
* `noetic-viz`
* `noetic-desktop`
* `noetic-desktop-full`

# Comparison to osrf/docker_images

This repo is a spiritual fork of [the official OSRF docker images](https://github.com/osrf/docker_images).
The image definitions were copied and modified from the official ones.
Why a new repository instead of contributing to the official images?

Two reasons:

    1. To make new images available sooner after ROS packages are synced.
        This has been [a longstanding issue with the official OSRF Docker images](https://github.com/osrf/docker_images/issues/112) that can't easily be solved due to both [Docker Official Library](https://github.com/docker-library/official-images) policies and how the ROS buildfarm versions packages on different architectures.
    2. To make it easier to modify the images by NOT generating them from templates.

Here is what is different:

    1. Images are rebuilt weekly.
    2. The `Containerfile`s are hand written, not generated from templates.
    3. Images are hosted on Github Packages, not [Docker Hub](https://hub.docker.com/).
    4. Images are defined using [Containerfile](https://github.com/containers/common/blob/main/docs/Containerfile.5.md)s instead of `Dockerfile`s
