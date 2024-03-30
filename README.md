# ROS Open Container Initiative Images

[Open Container Initiative](https://opencontainers.org/) images for [ROS](https://ros.org)!


Are you looking for **Docker images**?
You're in the right spot!
OCI images are Docker images.
[Here's how Docker and OCI relate](https://www.docker.com/blog/demystifying-open-container-initiative-oci-specifications/).


## Quick Start

New to containers? Start with [Docker](https://docs.docker.com/get-docker/). It has the most documentation and tutorials.

```
docker run --rm=true -ti ghcr.io/sloretz/ros:rolling-desktop ros2 --help
```

## About the images

All images are updated once per week at midnight GMT on Sunday.
Additionally each ROS distro's images are updated automatically after a sync.

The ROS 2 distros have an image for each [variant defined by REP 2001](https://ros.org/reps/rep-2001.html).
The ROS 1 distro [ROS Noetic](https://wiki.ros.org/noetic) has an image for each [metapackage defined by REP 142](https://www.ros.org/reps/rep-0142.html).
All images are based on Ubuntu.

| Image           | amd64 | arm v7 | arm64 v8 | Full Image Name                            |
|-----------------|-------|--------|----------|--------------------------------------------|
| [ROS Humble](http://docs.ros.org/en/humble)                                                 |
| ros-core        | ✅     | ❌      | ✅        | `ghcr.io/sloretz/ros:humble-ros-core`      |
| ros-base        | ✅     | ❌      | ✅        | `ghcr.io/sloretz/ros:humble-ros-base`      |
| desktop         | ✅     | ❌      | ✅        | `ghcr.io/sloretz/ros:humble-desktop`       |
| perception      | ✅     | ❌      | ✅        | `ghcr.io/sloretz/ros:humble-perception`    |
| simulation      | ✅     | ❌      | ✅        | `ghcr.io/sloretz/ros:humble-simulation`    |
| desktop-full    | ✅     | ❌      | ✅        | `ghcr.io/sloretz/ros:humble-desktop-full`  |
| [ROS Iron](http://docs.ros.org/en/iron)                                                     |
| ros-core        | ✅     | ❌      | ✅        | `ghcr.io/sloretz/ros:iron-ros-core`        |
| ros-base        | ✅     | ❌      | ✅        | `ghcr.io/sloretz/ros:iron-ros-base`        |
| desktop         | ✅     | ❌      | ✅        | `ghcr.io/sloretz/ros:iron-desktop`         |
| perception      | ✅     | ❌      | ✅        | `ghcr.io/sloretz/ros:iron-perception`      |
| simulation      | ✅     | ❌      | ✅        | `ghcr.io/sloretz/ros:iron-simulation`      |
| desktop-full    | ✅     | ❌      | ✅        | `ghcr.io/sloretz/ros:iron-desktop-full`    |
| [ROS Rolling](http://docs.ros.org/en/rolling)                                               |
| ros-core        | ✅     | ❌      | ✅        | `ghcr.io/sloretz/ros:rolling-ros-core`     |
| ros-base        | ✅     | ❌      | ✅        | `ghcr.io/sloretz/ros:rolling-ros-base`     |
| desktop         | ✅     | ❌      | ✅        | `ghcr.io/sloretz/ros:rolling-desktop`      |
| perception      | ✅     | ❌      | ✅        | `ghcr.io/sloretz/ros:rolling-perception`   |
| simulation      | ❌⚠️    | ❌      | ❌⚠️       | `ghcr.io/sloretz/ros:rolling-simulation`   |
| desktop-full    | ❌⚠️    | ❌      | ❌⚠️       | `ghcr.io/sloretz/ros:rolling-desktop-full` |
| [ROS Noetic](https://wiki.ros.org/noetic)                                                   |
| ros-core        | ✅     | ✅      | ✅        | `ghcr.io/sloretz/ros:noetic-ros-core`      |
| ros-base        | ✅     | ✅      | ✅        | `ghcr.io/sloretz/ros:noetic-ros-base`      |
| desktop         | ✅     | ✅      | ✅        | `ghcr.io/sloretz/ros:noetic-desktop`       |
| perception      | ✅     | ✅      | ✅        | `ghcr.io/sloretz/ros:noetic-perception`    |
| simulators      | ✅     | ❌      | ✅        | `ghcr.io/sloretz/ros:noetic-simulators`    |
| desktop-full    | ✅     | ❌      | ✅        | `ghcr.io/sloretz/ros:noetic-desktop-full`  |
| robot           | ✅     | ✅      | ✅        | `ghcr.io/sloretz/ros:noetic-robot`         |
| viz             | ✅     | ✅      | ✅        | `ghcr.io/sloretz/ros:noetic-viz`           |


❌⚠️ [ROS Rolling desktop-full and simulation images are not available for Ubuntu Noble](https://github.com/sloretz/ros_oci_images/issues/2), but are expected to be available in the future.

## Using with other OCI compatible tools

Used containers for a while?
Other tools might be better fit your use case.

[Apptainer](https://apptainer.org/)

```
apptainer run docker://ghcr.io/sloretz/ros:rolling-desktop ros2 --help
```

[Distrobox](https://github.com/89luca89/distrobox) (Requires Docker or Podman to be installed)

```
distrobox create --image ghcr.io/sloretz/ros:rolling-desktop --name rolling-desktop
distrobox enter rolling-desktop
. /opt/ros/rolling/setup.bash
ros2 --help
```

[nerdctl](https://github.com/containerd/nerdctl) using [rootless mode](https://github.com/containerd/nerdctl?tab=readme-ov-file#rootless-mode).

```
nerdctl run --rm=true -ti ghcr.io/sloretz/ros:rolling-desktop ros2 --help
```

[Podman](https://podman.io/)

```
podman run --rm=true -ti ghcr.io/sloretz/ros:rolling-desktop ros2 --help
```

[Rocker](https://github.com/osrf/rocker) (requires Docker to be installed)

```
rocker ghcr.io/sloretz/ros:rolling-desktop ros2 -- --help
```

[Sarus](https://sarus.readthedocs.io/en/stable/#)

```
sarus pull ghcr.io/sloretz/ros:rolling-desktop
sarus run -t ghcr.io/sloretz/ros:rolling-desktop ros2 --help
```

[SingularityCE](https://sylabs.io/singularity/)

```
singularity run docker://ghcr.io/sloretz/ros:rolling-desktop ros2 --help
```

[Toolbox](https://containertoolbx.org/) (Requires Podman to be installed)

```
toolbox create --image ghcr.io/sloretz/ros:rolling-desktop rolling-desktop
toolbox enter rolling-desktop
. /opt/ros/rolling/setup.bash
ros2 --help
```

[x11docker](https://github.com/mviereck/x11docker) (Requires Podman, Docker, or nerdctl to be installed)

```bash
# Option 1: using podman
podman pull ghcr.io/sloretz/ros:rolling-desktop
# Option 2: using docker
docker pull ghcr.io/sloretz/ros:rolling-desktop
# Option 3: using nerdctl
nerdctl pull ghcr.io/sloretz/ros:rolling-desktop

# After pulling, run this to use RViz with gpu acceleration
x11docker --gpu ghcr.io/sloretz/ros:rolling-desktop rviz2
```

## Comparison to osrf/docker_images

This repo is a spiritual fork of [the official OSRF docker images](https://github.com/osrf/docker_images).
The image definitions here were copied and modified from them.
The goal of this repo is to make updated images available sooner.
This has been [a longstanding issue with the official OSRF Docker images](https://github.com/osrf/docker_images/issues/112) that can't easily be solved due to both [Docker Official Library](https://github.com/docker-library/official-images) policies and how the ROS buildfarm versions packages on different architectures.
