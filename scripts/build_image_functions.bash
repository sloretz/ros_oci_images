function build_single_package_image() {
    rosdistro=$1
    from=$2
    nameandtag=$3
    manifest=$4
    arch=$5
    package=$4

    container=$(buildah from --manifest $manifest --arch $arch $from)
    echo $container

    # Install ROS 2 packages
    buildah run $container -- apt-get update
    buildah run $container -- apt-get install -y --no-install-recommends $package

    # Cleanup unnecessary stuff
    buildah run $container -- rm -rf /var/lib/apt/lists/*

    # Tag the image.
    buildah commit $container $nameandtag
}

function ros2_build_ros_core() {
    rosdistro=$1
    from=$2
    nameandtag=$3
    manifest=$4
    arch=$5

    container=$(buildah from --manifest $manifest --arch $arch $from)
    echo $container

    # Setup timezone.
    buildah run $container -- sh -c "echo 'Etc/UTC' > /etc/timezone"
    buildah run $container -- ln -s /usr/share/zoneinfo/Etc/UTC /etc/localtime
    buildah run $container -- apt-get update
    buildah run $container -- apt-get install -q -y --no-install-recommends tzdata

    # Install packages needed for setting up keys.
    buildah run $container -- apt-get install -q -y --no-install-recommends dirmngr gnupg2

    # Setup keys to access ROS apt repository.
    key='C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654'
    buildah run $container -- mkdir /tmp/gnupghome
    buildah run $container -- gpg --homedir=/tmp/gnupghome --batch --keyserver keyserver.ubuntu.com --recv-keys "$key"
    buildah run $container -- mkdir -p /usr/share/keyrings
    buildah run $container -- gpg --homedir=/tmp/gnupghome --output /usr/share/keyrings/ros2-latest-archive-keyring.gpg --batch --export "$key"
    buildah run $container -- gpgconf --kill all
    buildah run $container -- rm -rf /tmp/gnupghome

    # Setup apt sources.list
    # TODO(sloretz) Base image version (jammy) is hardcoded here. How to eliminate it?
    buildah run $container -- bash -c "echo \"deb [ signed-by=/usr/share/keyrings/ros2-latest-archive-keyring.gpg ] http://packages.ros.org/ros2/ubuntu jammy main\" > /etc/apt/sources.list.d/ros2-latest.list"

    # Set environment variables.
    buildah config --env LANG=C.UTF-8 $container
    buildah config --env LC_ALL=C.UTF-8 $container
    buildah config --env ROS_DISTRO=$rosdistro $container

    # Install ROS 2 packages.
    buildah run $container -- apt-get update
    buildah run $container -- apt-get install -y --no-install-recommends ros-$rosdistro-ros-core

    # Create entrypoint script
    buildah run $container -- bash -c "echo '#!/bin/bash' > /ros_entrypoint.sh"
    buildah run $container -- bash -c "echo 'set -e' >> /ros_entrypoint.sh"
    buildah run $container -- bash -c "echo >> /ros_entrypoint.sh"
    buildah run $container -- bash -c "echo '# Setup ROS 2 environment' >> /ros_entrypoint.sh"
    buildah run $container -- bash -c "echo >> /ros_entrypoint.sh"
    buildah run $container -- bash -c "echo 'source "/opt/ros/$rosdistro/setup.bash" --' >> /ros_entrypoint.sh"
    buildah run $container -- bash -c "echo 'exec \"\$@\"'>> /ros_entrypoint.sh"
    buildah run $container -- chmod +x /ros_entrypoint.sh
    buildah config --entrypoint '["/ros_entrypoint.sh"]' $container
    buildah config --cmd /bin/bash $container

    # Cleanup unnecessary stuff
    buildah run $container -- rm -rf /var/lib/apt/lists/*

    # Tag the image.
    buildah commit $container $nameandtag
}

function ros2_build_ros_base() {
    rosdistro=$1
    from=$2
    nameandtag=$3
    manifest=$4
    arch=$5

    container=$(buildah from --manifest $manifest --arch $arch $from)
    echo $container

    # Install bootstrap tools
    buildah run $container -- apt-get update
    buildah run $container -- apt-get install --no-install-recommends -y \
                                build-essential \
                                git \
                                python3-colcon-common-extensions \
                                python3-colcon-mixin \
                                python3-rosdep \
                                python3-vcstool

    # Bootstrap rosdep
    buildah run $container -- rosdep init
    buildah run $container -- rosdep update --rosdistro $rosdistro

    # Setup colcon mixin and metadata
    buildah run $container -- colcon mixin add default \
      https://raw.githubusercontent.com/colcon/colcon-mixin-repository/master/index.yaml
    buildah run $container -- colcon mixin update
    buildah run $container -- colcon metadata add default \
      https://raw.githubusercontent.com/colcon/colcon-metadata-repository/master/index.yaml
    buildah run $container -- colcon metadata update

    # Install ROS 2 packages
    buildah run $container -- apt-get install -y --no-install-recommends ros-$rosdistro-ros-base

    # Cleanup unnecessary stuff
    buildah run $container -- rm -rf /var/lib/apt/lists/*

    # Tag the image.
    buildah commit $container $nameandtag
}

function build_desktop() {
    rosdistro=$1
    from=$2
    nameandtag=$3
    manifest=$4
    arch=$5

    build_single_package_image $rosdistro $from $nameandtag $manifest $arch ros-$rosdistro-desktop
}

function build_desktop_full() {
    rosdistro=$1
    from=$2
    nameandtag=$3
    manifest=$4
    arch=$5

    build_single_package_image $rosdistro $from $nameandtag $manifest $arch ros-$rosdistro-desktop-full
}

function build_perception() {
    rosdistro=$1
    from=$2
    nameandtag=$3
    manifest=$4
    arch=$5

    build_single_package_image $rosdistro $from $nameandtag $manifest $arch ros-$rosdistro-perception
}

function ros2_build_simulation() {
    rosdistro=$1
    from=$2
    nameandtag=$3
    manifest=$4
    arch=$5

    build_single_package_image $rosdistro $from $nameandtag $manifest $arch ros-$rosdistro-simulation
}

function ros1_build_ros_core() {
    rosdistro=$1
    from=$2
    nameandtag=$3
    manifest=$4
    arch=$5

    container=$(buildah from --manifest $manifest --arch $arch $from)
    echo $container

    # Setup timezone.
    buildah run $container -- sh -c "echo 'Etc/UTC' > /etc/timezone"
    buildah run $container -- ln -s /usr/share/zoneinfo/Etc/UTC /etc/localtime
    buildah run $container -- apt-get update
    buildah run $container -- apt-get install -q -y --no-install-recommends tzdata

    # Install packages needed for setting up keys.
    buildah run $container -- apt-get install -q -y --no-install-recommends dirmngr gnupg2

    # Setup keys to access ROS apt repository.
    key='C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654'
    buildah run $container -- mkdir /tmp/gnupghome
    buildah run $container -- gpg --homedir=/tmp/gnupghome --batch --keyserver keyserver.ubuntu.com --recv-keys "$key"
    buildah run $container -- mkdir -p /usr/share/keyrings
    buildah run $container -- gpg --homedir=/tmp/gnupghome --output /usr/share/keyrings/ros1-latest-archive-keyring.gpg --batch --export "$key"
    buildah run $container -- gpgconf --kill all
    buildah run $container -- rm -rf /tmp/gnupghome

    # Setup apt sources.list
    # TODO(sloretz) Base image version (focal) is hardcoded here. How to eliminate it?
    buildah run $container -- bash -c "echo \"deb [ signed-by=/usr/share/keyrings/ros1-latest-archive-keyring.gpg ] http://packages.ros.org/ros/ubuntu focal main\" > /etc/apt/sources.list.d/ros1-latest.list"

    # Set environment variables.
    buildah config --env LANG=C.UTF-8 $container
    buildah config --env LC_ALL=C.UTF-8 $container
    buildah config --env ROS_DISTRO=$rosdistro $container

    # Install ROS 1 packages.
    buildah run $container -- apt-get update
    buildah run $container -- apt-get install -y --no-install-recommends ros-$rosdistro-ros-core

    # Create entrypoint script
    buildah run $container -- bash -c "echo '#!/bin/bash' > /ros_entrypoint.sh"
    buildah run $container -- bash -c "echo 'set -e' >> /ros_entrypoint.sh"
    buildah run $container -- bash -c "echo >> /ros_entrypoint.sh"
    buildah run $container -- bash -c "echo '# Setup ROS environment' >> /ros_entrypoint.sh"
    buildah run $container -- bash -c "echo >> /ros_entrypoint.sh"
    buildah run $container -- bash -c "echo 'source "/opt/ros/$rosdistro/setup.bash" --' >> /ros_entrypoint.sh"
    buildah run $container -- bash -c "echo 'exec \"\$@\"'>> /ros_entrypoint.sh"
    buildah run $container -- chmod +x /ros_entrypoint.sh
    buildah config --entrypoint '["/ros_entrypoint.sh"]' $container
    buildah config --cmd /bin/bash $container

    # Cleanup unnecessary stuff
    buildah run $container -- rm -rf /var/lib/apt/lists/*

    # Tag the image.
    buildah commit $container $nameandtag
}

function ros1_build_ros_base() {
    rosdistro=$1
    from=$2
    nameandtag=$3
    manifest=$4
    arch=$5

    container=$(buildah from --manifest $manifest --arch $arch $from)
    echo $container

    # Install bootstrap tools
    buildah run $container -- apt-get update
    buildah run $container -- apt-get install --no-install-recommends -y \
                                build-essential \
                                python3-rosdep \
                                python3-rosinstall \
                                python3-vcstools

    # Bootstrap rosdep
    buildah run $container -- rosdep init
    buildah run $container -- rosdep update --rosdistro $rosdistro

    # Install ROS packages
    buildah run $container -- apt-get install -y --no-install-recommends $manifest $arch ros-$rosdistro-ros-base

    # Cleanup unnecessary stuff
    buildah run $container -- rm -rf /var/lib/apt/lists/*

    # Tag the image.
    buildah commit $container $nameandtag
}

function ros1_build_simulators() {
    rosdistro=$1
    from=$2
    nameandtag=$3
    manifest=$4
    arch=$5

    build_single_package_image $rosdistro $from $nameandtag $manifest $arch ros-$rosdistro-simulators
}

function ros1_build_robot() {
    rosdistro=$1
    from=$2
    nameandtag=$3
    manifest=$4
    arch=$5

    build_single_package_image $rosdistro $from $nameandtag $manifest $arch ros-$rosdistro-robot
}

function ros1_build_viz() {
    rosdistro=$1
    from=$2
    nameandtag=$3
    manifest=$4
    arch=$5

    build_single_package_image $rosdistro $from $nameandtag $manifest $arch ros-$rosdistro-viz
}