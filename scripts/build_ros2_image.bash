#!/bin/bash
set -eux -o pipefail


function build_ros_core() {
    rosdistro=$1
    from=$2
    nameandtag=$3

    container=$(buildah from $from)
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
    buildah run $container -- bash -c 'echo "deb [ signed-by=/usr/share/keyrings/ros2-latest-archive-keyring.gpg ] http://packages.ros.org/ros2/ubuntu jammy main" > /etc/apt/sources.list.d/ros2-latest.list'

    # Set environment variables.
    buildah config --env LANG=C.UTF-8 $container
    buildah config --env LC_ALL=C.UTF-8 $container
    buildah config --env ROS_DISTRO=$rosdistro $container

    # Install ROS 2 packages.
    buildah run $container -- apt-get update
    buildah run $container -- apt-get install -y --no-install-recommends ros-humble-ros-core

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

build_ros_core humble ubuntu:jammy ros_oci_images:humble-ros-core