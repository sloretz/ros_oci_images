# ROS 2 Dev Container Images

This folder contains definitions for ROS 2 [dev containers](https://containers.dev/).
Dev containers make it easy to develop software for an operating system (OS) than is different from the one your computer uses, without having to use a virtual machine.
If you haven't used one before, [read the VS Code documentation to learn more](https://code.visualstudio.com/docs/devcontainers/containers).

## Images to build ROS 2 from source

These images are updated once per week at midnight GMT on Sunday.

| In-container OS | amd64 | arm v7 | arm64 v8 | Full Image Name                                | ROS distro compatibility |
|-------------------|-------|--------|----------|------------------------------------------------|--------------------------|
| Ubuntu Jammy      | ✅     | ✅      | ✅        | `ghcr.io/sloretz/ros-dev:ubuntu-jammy`      | Humble, Iron             |
| Ubuntu Noble      | ✅     | ✅      | ✅        | `ghcr.io/sloretz/ros-dev:ubuntu-noble`      | Jazzy, Rolling           |

## Using a dev container

1. [Install Visual Studio Code](https://code.visualstudio.com/download)
1. [Install the Visual Studio Code Dev Container extension](https://code.visualstudio.com/docs/devcontainers/containers#_installation)
1. [Install Docker](https://www.docker.com/get-started/)
1. [Add yourself to the `docker` group](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user)


Follow these instructions to create a dev container from one of these images.

1. Create a file at `.devcontainer/devcontainer.json`
    ```bash
    mkdir .devcontainer
    touch .devcontainer/devcontainer.json
    ```
1. Specify the image you want to use in the `devcontainer.json` file using this template.
   ```json
    {
        "name": "My Dev Container",
        "image": "ghcr.io/sloretz/ros-dev:ubuntu-noble",
        "remoteUser": "ros"
    }
    ```
1. Open [VS Code](https://code.visualstudio.com/)
    ```bash
    code .
    ```
1. Type `ctrl` + `shift` + `p` and Choose `Dev Containers: Reopen in Container` from the drop down at the top of VS Code.


Congratulations!
You are now in a dev container.

## Building ROS 2 from source in a dev container

Follow these instructions to build ROS from source inside one of these images:

1. Clone the branch belonging to the ROS distro you want to build from [ros2/ros2](https://github.com/ros2/ros2)
    ```bash
    git clone -b rolling https://github.com/ros2/ros2.git
    ```
1. Create a `.devcontainer/devcontainer.json` as described above
    ```bash
    cd ros2
    mkdir .devcontainer
    touch .devcontainer/devcontainer.json
    ```
1. Specify the image you want to use in the `devcontainer.json` file using this template.
   ```json
    {
        "name": "ROS Roling from source",
        "image": "ghcr.io/sloretz/ros-dev:ubuntu-noble",
        "remoteUser": "ros"
    }
    ```
1. Enter the dev container as described above
1. Import all the source code using [vsctool](https://github.com/dirk-thomas/vcstool)
    ```bash
    vcs import --input ros2.repos src/
    ```
1. Install all system dependencies using [rosdep](https://docs.ros.org/en/rolling/Tutorials/Intermediate/Rosdep.html)
    ```bash
    sudo apt-get update && \
    rosdep install -ryi --from-paths src
    ```
    Type `yes` when asked to accept the RTI Connext license.
1. Build the entire workspace using [colcon](https://colcon.readthedocs.io/en/released/)
    ```bash
    colcon build
    ```


## Troubleshooting

### No files visible in VS Code

If you don't see any files in VS Code after opening the dev container, you might be affected by https://github.com/microsoft/vscode-remote-release/issues/1333 .
Add the following options to `devcontainer.json` to [configure the selinux label](https://docs.docker.com/storage/bind-mounts/#configure-the-selinux-label).

```json
    "workspaceMount": "",
    "runArgs": ["--volume=${localWorkspaceFolder}:/workspaces/${localWorkspaceFolderBasename}:Z"]
```