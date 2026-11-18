ARG UBUNTU_IMAGE=ubuntu:noble

FROM ${UBUNTU_IMAGE} AS ros-core

ARG ROS_DISTRO=jazzy
ARG use_testing_repo=false

# Setup timezone
RUN echo 'Etc/UTC' > /etc/timezone && \
    ln -sf /usr/share/zoneinfo/Etc/UTC /etc/localtime

# Install packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    jq \
    lsb-release \
    && rm -rf /var/lib/apt/lists/*

# Setup keys and apt sources
RUN set -eux; \
    export ROS_APT_SOURCE_VERSION=$(curl --retry 5 -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | jq -r ".tag_name"); \
    if [ "${use_testing_repo}" = "true" ]; then \
        curl --retry 5 -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-testing-apt-source_${ROS_APT_SOURCE_VERSION}.$(lsb_release -sc)_all.deb"; \
    else \
        curl --retry 5 -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(lsb_release -sc)_all.deb"; \
    fi; \
    apt-get install -y /tmp/ros2-apt-source.deb; \
    rm /tmp/ros2-apt-source.deb

# Setup environment
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV ROS_DISTRO=${ROS_DISTRO}

# Install ROS packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-${ROS_DISTRO}-ros-core \
    && rm -rf /var/lib/apt/lists/*

# Setup entrypoint
COPY ./ros_entrypoint.sh /

ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]


FROM ros-core AS ros-base

# Install bootstrap tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    python3-colcon-common-extensions \
    python3-colcon-mixin \
    python3-rosdep \
    python3-vcstool \
    && rm -rf /var/lib/apt/lists/*

# Bootstrap rosdep
RUN rosdep init && \
    rosdep update --rosdistro ${ROS_DISTRO}

# Setup colcon mixin and metadata
RUN colcon mixin add default \
    https://raw.githubusercontent.com/colcon/colcon-mixin-repository/master/index.yaml && \
    colcon mixin update && \
    colcon metadata add default \
    https://raw.githubusercontent.com/colcon/colcon-metadata-repository/master/index.yaml && \
    colcon metadata update

# Install ROS packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-${ROS_DISTRO}-ros-base \
    && rm -rf /var/lib/apt/lists/*


FROM ros-base AS desktop

RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-${ROS_DISTRO}-desktop \
    && rm -rf /var/lib/apt/lists/*


FROM ros-base AS perception

RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-${ROS_DISTRO}-perception \
    && rm -rf /var/lib/apt/lists/*


FROM ros-base AS simulation

RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-${ROS_DISTRO}-simulation \
    && rm -rf /var/lib/apt/lists/*


FROM desktop AS desktop-full

RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-${ROS_DISTRO}-desktop-full \
    && rm -rf /var/lib/apt/lists/*
