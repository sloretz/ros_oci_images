# Copyright 2024 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

ARG ROS_DISTRO=rolling
ARG FROM=ros:${ROS_DISTRO}-desktop

FROM ${FROM}

# Must redeclare so that value is available after FROM statement.
ARG ROS_DISTRO

# Setup apt sources.list for testing
RUN echo "deb [ signed-by=/usr/share/keyrings/ros2-latest-archive-keyring.gpg ] http://packages.ros.org/ros2-testing/ubuntu `lsb_release -sc` main" > /etc/apt/sources.list.d/ros2-testing.list

RUN cat /etc/apt/sources.list.d/ros2-testing.list

# Upgrade all packages to versions in ros2-testing
RUN apt-get update && apt-get dist-upgrade -yy \
    && rm -rf /var/lib/apt/lists/*