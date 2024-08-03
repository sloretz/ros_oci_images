VERSION 0.8

IMPORT ./apt AS apt

noetic:
    ARG registry='localhost/'
    ARG ROS_DISTRO='noetic'
    ARG UBUNTU_IMAGE='ubuntu:focal'

    # ros-core
    FROM --pass-args +ros-core
    SAVE IMAGE --push ${registry}ros:${ROS_DISTRO}-ros-core

    # ros-base
    FROM --pass-args +ros-base
    SAVE IMAGE --push ${registry}ros:${ROS_DISTRO}-ros-base

    # robot
    FROM --pass-args +robot
    SAVE IMAGE --push ${registry}ros:${ROS_DISTRO}-robot

    # desktop
    FROM --pass-args +desktop
    SAVE IMAGE --push ${registry}ros:${ROS_DISTRO}-desktop

    # perception
    FROM --pass-args +perception
    SAVE IMAGE --push ${registry}ros:${ROS_DISTRO}-perception

    # simulators
    FROM --pass-args +simulators
    SAVE IMAGE --push ${registry}ros:${ROS_DISTRO}-simulators

    # simulators-osrf
    FROM --pass-args +simulators-osrf
    SAVE IMAGE --push ${registry}ros:${ROS_DISTRO}-simulators-osrf

    # desktop-full
    FROM --pass-args +desktop-full
    SAVE IMAGE --push ${registry}ros:${ROS_DISTRO}-desktop-full

    # viz
    FROM --pass-args +viz
    SAVE IMAGE --push ${registry}ros:${ROS_DISTRO}-viz


viz:
    ARG ROS_DISTRO
    FROM --pass-args +ros-base
    DO apt+INSTALL --packages=ros-${ROS_DISTRO}-viz
    SAVE IMAGE localhost/ros-intermediate:${ROS_DISTRO}-viz


desktop-full:
    ARG ROS_DISTRO
    FROM --pass-args +desktop
    DO apt+INSTALL --packages=ros-${ROS_DISTRO}-desktop-full
    SAVE IMAGE localhost/ros-intermediate:${ROS_DISTRO}-desktop-full


simulators-osrf:
    ARG ROS_DISTRO

    FROM --pass-args +simulators

    # setup keys
    RUN set -eux; \
        key='D2486D2DD83DB69272AFE98867170598AF249743'; \
        export GNUPGHOME="$(mktemp -d)"; \
        gpg --batch --keyserver keyserver.ubuntu.com --recv-keys "$key"; \
        mkdir -p /usr/share/keyrings; \
        gpg --batch --export "$key" > /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg; \
        gpgconf --kill all; \
        rm -rf "$GNUPGHOME"

    # setup osrf sources.list
    RUN . /etc/os-release \
        && echo "deb [ signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg ] http://packages.osrfoundation.org/gazebo/ubuntu-stable focal main" > /etc/apt/sources.list.d/gazebo-latest.list

    # update gazebo packages from osrf repo
    RUN apt-get update && apt-get dist-upgrade -yy \
    && rm -rf /var/lib/apt/lists/*

    SAVE IMAGE localhost/ros-intermediate:${ROS_DISTRO}-simulators-osrf


simulators:
    ARG ROS_DISTRO
    FROM --pass-args +robot
    DO apt+INSTALL --packages=ros-${ROS_DISTRO}-simulators
    SAVE IMAGE localhost/ros-intermediate:${ROS_DISTRO}-simulators


perception:
    ARG ROS_DISTRO
    FROM --pass-args +ros-base
    DO apt+INSTALL --packages=ros-${ROS_DISTRO}-perception
    SAVE IMAGE localhost/ros-intermediate:${ROS_DISTRO}-perception


desktop:
    ARG ROS_DISTRO
    FROM --pass-args +robot
    DO apt+INSTALL --packages=ros-${ROS_DISTRO}-desktop
    SAVE IMAGE localhost/ros-intermediate:${ROS_DISTRO}-desktop


robot:
    ARG ROS_DISTRO
    FROM --pass-args +ros-base
    DO apt+INSTALL --packages=ros-${ROS_DISTRO}-robot
    SAVE IMAGE localhost/ros-intermediate:${ROS_DISTRO}-robot


ros-base:
    ARG ROS_DISTRO

    FROM --pass-args +ros-core

    # install bootstrap tools
    DO apt+INSTALL --packages="
        build-essential 
        python3-rosdep
        python3-rosinstall
        python3-vcstools
        ca-certificates"

    # Bootstrap rosdep
    # Workaround https://github.com/ros-infrastructure/rosdep/issues/934
    RUN sudo update-ca-certificates --fresh
    RUN rosdep init && rosdep update --rosdistro $ROS_DISTRO

    # install ros packages
    DO apt+INSTALL --packages=ros-${ROS_DISTRO}-ros-base

    SAVE IMAGE localhost/ros-intermediate:${ROS_DISTRO}-ros-base


ros-core:
    ARG UBUNTU_IMAGE
    ARG ROS_DISTRO

    FROM $UBUNTU_IMAGE

    # Setup timezone
    RUN echo 'Etc/UTC' > /etc/timezone && \
        ln -s /usr/share/zoneinfo/Etc/UTC /etc/localtime

    # Install packages
    DO apt+INSTALL --packages="
        tzdata
        dirmngr
        gnupg2
        lsb-release"

    # Setup keys
    RUN set -eux; \
        key='C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654'; \
        export GNUPGHOME="$(mktemp -d)"; \
        gpg --batch --keyserver keyserver.ubuntu.com --recv-keys "$key"; \
        mkdir -p /usr/share/keyrings; \
        gpg --batch --export "$key" > /usr/share/keyrings/ros1-latest-archive-keyring.gpg; \
        gpgconf --kill all; \
        rm -rf "$GNUPGHOME"

    # Setup sources.list
    RUN echo "deb [ signed-by=/usr/share/keyrings/ros1-latest-archive-keyring.gpg ] http://packages.ros.org/ros/ubuntu `lsb_release -sc` main" > /etc/apt/sources.list.d/ros1-latest.list

    # Setup environment
    ENV LANG C.UTF-8
    ENV LC_ALL C.UTF-8

    ENV ROS_DISTRO ${ROS_DISTRO}

    # Install ROS packages
    DO apt+INSTALL --packages=ros-${ROS_DISTRO}-ros-core

    # Setup entrypoint
    COPY ./ros1/ros-core/ros_entrypoint.sh /

    ENTRYPOINT ["/ros_entrypoint.sh"]
    CMD ["bash"]
    SAVE IMAGE localhost/ros-intermediate:${ROS_DISTRO}-ros-core
