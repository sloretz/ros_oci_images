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

ARG ROS_DISTRO=noetic
ARG FROM=ros:${ROS_DISTRO}-simulators

FROM ${FROM}

# Must redeclare so that value is available after FROM statement.
ARG ROS_DISTRO

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
