# Contribution Guide

Thank you for being willing to help!

## How to make a Documentation Contribution

This repo uses [Markdown](https://www.markdownguide.org/) for its documentation.
These files have the extension `.md`.
When adding to these files please **put each sentence on its own line**.
This style makes it easier to review changes to the documentation.

```markdown
# This is a title

Please put one sentence per line.
Yes, like this.
Thank you!
```

If you would like to add a tutorial, please consider contributing it to [the official ROS 2 Documentation](https://github.com/ros2/ros2_documentation).
If it's not accepted there, then please create an issue on this repository and we can work together to figure out where to put it.

## How to make a source code contribution

### Install the required versions of dependencies

Required to build images:

* `qemu-user-static` version 6.2
* `buildah` version 1.34.0

Required to test images:

* `podman` Not sure what version, but both versions 3.4.4 and 4.9.0 have worked for me.

Required to lint source code:

* `black` - any 2024 version.

The best way to get these dependencies is to use Ubuntu 22.04 (Jammy).
First, install `qemu-user-static` via `sudo apt install qemu-user-static`.
Second, [build and install buildah from source](https://github.com/containers/buildah/blob/v1.34.0/install.md#building-from-scratch).

There is a script to install the build dependencies: `./scripts/install_dependencies.bash`

### Understand How the repository is structured

Understanding where everything is will help you make a contribution.

At a high level, this repository uses [Python](https://www.python.org/about/gettingstarted/) scripts to invoke [buildah](https://buildah.io/) to build images from [Containerfiles](https://github.com/containers/common/blob/main/docs/Containerfile.5.md).
The python script is called using [Github Actions](https://github.com/features/actions) to build images for each active [ROS distro](http://docs.ros.org/en/rolling/Releases.html).
The images are pushed to [Github Packages](https://github.com/features/packages).
Afterwards anyone can pull the image they need and run it.

#### What's in the ros1 and ros2 folders

The `ros1` and `ros2` folders hold [Containerfile](https://github.com/containers/common/blob/main/docs/Containerfile.5.md) definitions for ROS 1 and ROS 2 respectively.
A `Containerfile`'s syntax is identical to a `Dockerfile`'s syntax.

```
ros1
├── desktop
│   └── Containerfile
├── desktop-full
│   └── Containerfile
├── perception
│   └── Containerfile
├── robot
│   └── Containerfile
├── ros-base
│   └── Containerfile
├── ros-core
│   ├── Containerfile
│   └── ros_entrypoint.sh
├── simulators
│   └── Containerfile
└── viz
    └── Containerfile
```

```
ros2
├── desktop
│   └── Containerfile
├── desktop-full
│   └── Containerfile
├── perception
│   └── Containerfile
├── ros-base
│   └── Containerfile
├── ros-core
│   ├── Containerfile
│   └── ros_entrypoint.sh
└── simulation
    └── Containerfile
```

Originally the files in `ros1` were taken from [here](https://github.com/osrf/docker_images/tree/3d7df313d1b9be171f5aa87b5daa097354f753ea/ros/noetic/ubuntu/focal), and the ROS 2 definitions  were taken from [here](https://github.com/osrf/docker_images/tree/3d7df313d1b9be171f5aa87b5daa097354f753ea/ros/rolling/ubuntu/jammy).
The files don't need to match the ones in [osrf/docker_images](https://github.com/osrf/docker_images) exactly, but they should stay close.

In the `ros1` folder each subfolder is named after a [metapackage defined by REP 142](https://www.ros.org/reps/rep-0142.html).
In the `ros2` folder each subfolder is named after a [variant defined by REP 2001](https://ros.org/reps/rep-2001.html).
If you think there should be a new folder in `ros2` (ex: a navigation image with Nav2, or a moveit2 image) then please [propose a new variant to REP 2001 first](https://github.com/ros-infrastructure/rep/blob/master/rep-2001.rst) as a pull request to the [ros-infrastructure/rep repo](https://github.com/ros-infrastructure/rep).
After it's accepted we can create an image for it here.
If you think there should be a new ROS 1 image, I would suggest not creating one.
[ROS 1 is nearly end of life](https://endoflife.date/ros) and should be kept stable.

#### What's in the scripts folder

The `scripts` folder holds Python and Bash scripts used for building and testing the images

```
scripts/
├── build_images.py
├── install_dependencies.bash
└── test_images.py
```

The file `build_images.py` invokes buildah to create all images for one ROS distro.
Inside it is hardcoded knowledge of what architectures are supported by each ROS distro.
Run `./scripts/build_images.py --help` to see what options it takes.

The file `test_images.py` invokes podman to run commands in all images for one ROS distro.
Inside it is another hardcoded copy of the knowledge of what architectures are supported by each ROS distro.
Run `./scripts/test_images.py --help` to see what options it takes.

The `install_dependencies.bash` script installs the dependencies needed to build images on an Ubuntu 22.04 machine.

#### What's in the .github/workflows folder

This folder contains github workflows.
These are used to build and test the images.

```
.github/workflows/
├── build-and-deploy-all-if-necessary.yaml
├── build-and-deploy-all.yaml
├── build-and-deploy-one-ros-distro-if-necessary.yaml
├── build-and-deploy-one-ros-distro.yaml
├── python-lint.yaml
└── test-deployed-images-one-ros-distro.yaml
```

The workflow `test-deployed-images-one-ros-distro.yaml` pulls all images for a given ROS distro and makes sure the `ros2` command can be used.

The workflow `build-and-deploy-one-ros-distro.yaml` builds all images for a given ROS distro, pushes them to github actions, and then calls `test-deployed-images-one-ros-distro.yaml` to make sure they work.

The workflow `build-and-deploy-one-ros-distro-if-necessary.yaml` checks if a new version of the `ros-core` package is available, and if so calls `build-and-deploy-one-ros-distro.yaml` to update it.
This is probably a mistake.
It should likely check all images for a ROS distro and trigger the rebuild job if any of them have an update available.

The workflow `build-and-deploy-all-yaml` runs once per week and rebuilds all of the ROS images.

The workflow `build-and-deploy-all-if-necessary.yaml` runs every 6 hours and calls `build-and-deploy-one-ros-distro-if-necessary.yaml` for every supported ROS distro.

The workflow `python-lint.yaml` runs the [black Python linter](https://github.com/psf/black).
