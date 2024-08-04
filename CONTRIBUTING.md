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

Required to build and test images:

* `qemu-user-static` version 6.2
* `docker` not sure what version. 24.0.5 works.
* `earthly` version 0.8

Required to lint source code:

* `black` - any 2024 version.


### Understand How the repository is structured

This repo uses [Earthly](https://docs.earthly.dev/) to build and push OCI images from [Earthfiles](https://docs.earthly.dev/docs/earthfile).
The Earthfiles create OCI Images for each active [ROS distro](http://docs.ros.org/en/rolling/Releases.html).
The Earthfiles push the images to [Github Packages](https://github.com/features/packages).

There is a top-level Earthfile which imports from Earthfiles in subfolders.
The top-level Earthfile defines what platforms each ROS distro's images are built for.

The `ros1` and `ros2` folders each have an Earthfile used to create images with ROS 1 and ROS 2 installed from debian packages, respectively.
The ROS 1 images definitions were taken from [here](https://github.com/osrf/docker_images/tree/3d7df313d1b9be171f5aa87b5daa097354f753ea/ros/noetic/ubuntu/focal), and the ROS 2 definitions  were taken from [here](https://github.com/osrf/docker_images/tree/3d7df313d1b9be171f5aa87b5daa097354f753ea/ros/rolling/ubuntu/jammy).
The Earthfiles don't need to match the Dockerfiles in [osrf/docker_images](https://github.com/osrf/docker_images), but they should stay close.

The `ros1` Earthfile defines a target for ROS Noetic calle `noetic`.
That target builds an OCI image for each [metapackage defined by REP 142](https://www.ros.org/reps/rep-0142.html) plus `simulators-osrf`.
The `ros2` Earthfile defines a target for each active ROS 2 distro.
Eatch target creates an OCI image for each [variant defined by REP 2001](https://ros.org/reps/rep-2001.html).

If you think there should be a new folder in `ros2` (ex: a navigation image with Nav2, or a moveit2 image) then please [propose a new variant to REP 2001 first](https://github.com/ros-infrastructure/rep/blob/master/rep-2001.rst) as a pull request to the [ros-infrastructure/rep repo](https://github.com/ros-infrastructure/rep).
After it's accepted we can create an image for it here.
If you think there should be a new ROS 1 image, I would suggest not creating one.
[ROS 1 is nearly end of life](https://endoflife.date/ros) and should be kept stable.

#### What's in the scripts folder

The `scripts` folder holds miscellaneous scripts used by the github actions in this repository.


The file `test_images.py` invokes docker to run commands in all images for one ROS distro.
Inside it is another hardcoded copy of the knowledge of what architectures are supported by each ROS distro.
Run `./scripts/test_images.py --help` to see what options it takes.

The `install_dependencies.bash` script installs `qemu-user-static` on an Ubuntu 22.04 machine.

The `is_new_version_available.py` script checks if there's a new verion of a debian package.
This is used to determine when new images need to be built after a ROS distro's packages get sync'd to the main apt repo.

#### What's in the .github/workflows folder

This folder contains github workflows.
These are used to build and test the images.

The workflow `test-deployed-images-one-ros-distro.yaml` pulls all images for a given ROS distro and makes sure the `ros2` command can be used.

The workflow `build-and-deploy-one-ros-distro.yaml` builds all images for a given ROS distro, pushes them to github actions, and then calls `test-deployed-images-one-ros-distro.yaml` to make sure they work.

The workflow `build-and-deploy-one-ros-distro-if-necessary.yaml` checks if a new version of the `ros-$distro-desktop-full` package is available, and if so calls `build-and-deploy-one-ros-distro.yaml` to update it.

The workflow `build-and-deploy-all-yaml` runs once per week and rebuilds all of the ROS images.

The workflow `build-and-deploy-all-if-necessary.yaml` runs every 6 hours and calls `build-and-deploy-one-ros-distro-if-necessary.yaml` for every supported ROS distro.

The workflow `python-lint.yaml` runs the [black Python linter](https://github.com/psf/black).

The workflow `ci-build-amd64-image-one-ros-distro.yaml` builds the amd64 architecture images for one ROS distro, and the workflow `ci-build-amd64-images.yaml` calls it for every supported ROS distro.
