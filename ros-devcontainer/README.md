# ROS Devcontainer

This directory is used to build images for [Visual Studio Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers).
They come ready to [build ROS 2 from source](http://docs.ros.org/en/rolling/Installation.html#building-from-source), but they can also be used to build packages on top of a binary installation.

All images come with a non-root user called `ros-developer` with user and group ids of `1000`.
The `ros-developer` user is configured for passwordless use of `sudo`.

## Prerequisites

1. [Install Visual Studio Code](https://code.visualstudio.com/download)
1. [Install the Visual Studio Code Dev Container extension](https://code.visualstudio.com/docs/devcontainers/containers#_installation)
1. [Install Docker](https://www.docker.com/get-started/)
1. [Add yourself to the `docker` group](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user)

## Use case: Building all of ROS 2 from source

Here's how to use the dev container to [build ROS 2 from source](http://docs.ros.org/en/rolling/Installation.html#building-from-source).

### 1. Clone https://github.com/ros2/ros2

Clone https://github.com/ros2/ros2 and setup the bare minimum for a workspace.

```
git clone https://github.com/ros2/ros2.git
cd ros2
mkdir src
```

### 2. Create a .devcontainer/devcontainer.json file

Create a folder called `.devcontainer` Inside of the `ros2` folder.

```
mkdir .devcontainer
```

Create a file called `devcontainer.json` within the `.devcontainer` folder.

```
touch .devcontainer/devcontainer.json
```

Put the following content into `.devcontainer/devcontainer.json`.

```json
{
    "image": "ghcr.io/sloretz/ros-devcontainer:ubuntu-jammy",
    "containerEnv": {
        "ROS_AUTOMATIC_DISCOVERY_RANGE": "LOCALHOST"
    }
}
```

You don't technically need the `containerEnv` stuff that sets `ROS_AUTOMATIC_DISCOVERY_RANGE`, but it prevents you from accidentally communicating with other robots on the network until you're ready to.

### 3. Open the dev container with Visual Studio Code

Open a Visual Studio Code instance inside of the `ros2` folder.

```
code .
```

Open the dev container by hitting `CTRL` + `SHIFT` + `P` and start typing until you can click on the command `Dev Containers: Reopen in Container`.
Run that command!

Congratulations you've started the dev container! Usually this is where you'll start working on your code, but follow the next couple steps for first-time setup.

### 4. Clone the ROS 2 repos

[Open a terminal in Visual Studio Code](https://code.visualstudio.com/docs/terminal/basics).
You now have a working terminal inside the container.
Run the following command to clone all of the core ROS 2 repos from the `ros2` folder.

```
vcs import --from-paths ros2.repos src/
```

Run the following command to install all of the required system dependencies inside the container.

```
rosdep install --from-paths src --ignore-packages-from-source -ry
```

### 5. Perform the initial build

You now have a container ready to build ROS 2 from source.
Run the following command in the `ros2` folder to build all of it.

```
colcon build
```

## Use case: Developing your own ROS packages

Here's how to use the dev container to develop your own ROS packages.

### 1. Create your colcon workspace

If you don't already have one, create a colcon workspace.
```
mkdir ~/my_ws
cd ~/my_ws
mkdir src
```

Clone your packages into the `src` folder.

### 2. Create a .devcontainer/devcontainer.json file

Create a folder called `.devcontainer` Inside of the `ros2` folder.

```
mkdir .devcontainer
```

Create a file called `devcontainer.json` within the `.devcontainer` folder.

```
touch .devcontainer/devcontainer.json
```

Put the following content into `.devcontainer/devcontainer.json`.

```json
{
    "image": "ghcr.io/sloretz/ros-devcontainer:ubuntu-jammy",
    "containerEnv": {
        "ROS_AUTOMATIC_DISCOVERY_RANGE": "LOCALHOST"
    }
}
```

### 3. Open the dev container with Visual Studio Code

Open a Visual Studio Code instance inside of the `ros2` folder.

```
code .
```

Open the dev container by hitting `CTRL` + `SHIFT` + `P` and start typing until you can click on the command `Dev Containers: Reopen in Container`.
Run that command!

Congratulations you've started the dev container!

### 3. Install as much ROS as you need

Look, you know what dependencies your packages need.
That said it's helpful to have some tools for debugging, so go ahead and install the desktop package.

[Open a terminal in Visual Studio Code](https://code.visualstudio.com/docs/terminal/basics).
Assuming you want to develop in ROS Rollling, run the following commands in the terminal.

```
sudo apt-get install ros-rolling-desktop
```

Use rosdep to install any additional system dependencies needed by your workspace.


```
rosdep install --from-paths src --ignore-packages-from-source -y
```

## Troubleshooting

### Can't see any files in the dev container

If after you open the dev container you can't see any files in vscode, you might be affected by https://github.com/microsoft/vscode-remote-release/issues/1333 .
Add the following options to `devcontainer.json` to [configure the selinux label](https://docs.docker.com/storage/bind-mounts/#configure-the-selinux-label).

```json
    "workspaceMount": "",
    "runArgs": ["--volume=${localWorkspaceFolder}:/workspaces/${localWorkspaceFolderBasename}:Z"]
```