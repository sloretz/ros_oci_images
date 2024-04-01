#!/usr/bin/env python3

# Copyright 2024 Shane Loretz.
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

import argparse
import subprocess


# TODO(sloretz) share implementation with build_images.py
def _full_name(registry, name, tag):
    return f"{registry}/{name}:{tag}"


def _buildah_pull(full_name, dry_run):
    cmd = ["buildah", "pull", full_name]
    if dry_run:
        print(cmd)
    else:
        subprocess.check_call(cmd)


def _podman_run(full_name, extra_cmd, arch=None, variant=None, dry_run=False):
    cmd = ["podman", "run", "--rm=true", "-ti"]
    if arch:
        cmd.append("--arch")
        cmd.append(arch)
        if variant:
            cmd.append("--variant")
            cmd.append(variant)
    cmd.append(full_name)
    cmd.extend(extra_cmd)
    if dry_run:
        print(cmd)
    else:
        subprocess.check_call(cmd)


def _print_ros2_help(full_name, arch=None, variant=None, dry_run=False):
    cmd = ["ros2", "--help"]
    _podman_run(full_name, cmd, arch, variant, dry_run)


def _print_pkg_version(full_name, pkg, arch=None, variant=None, dry_run=False):
    cmd = ["apt-cache", "show", pkg]
    _podman_run(full_name, cmd, arch, variant, dry_run)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", default="localhost", type=str)
    parser.add_argument("--name", default="ros", type=str)
    parser.add_argument("--rosdistro", required=True, type=str)
    parser.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()

    return args


def main():
    args = parse_arguments()

    ros_distro = args.rosdistro.lower()
    dry_run = args.dry_run

    if "noetic" == ros_distro:
        # ROS 1
        suffixes = [
            "ros-core",
            "ros-base",
            "desktop",
            "perception",
            "simulators",
            "simulators-osrf",
            "desktop-full",
            "robot",
            "viz",
        ]
        architectures = [
            ("amd64", None),
            ("arm", "v7"),
            ("arm64", "v8"),
        ]
        for s in suffixes:
            s = "simulators" if s == "simulators-osrf" else s
            tag = f"{ros_distro}-{s}"
            package = f"ros-{ros_distro}-{s}"
            full_name = _full_name(args.registry, args.name, tag)
            for arch, variant in architectures:
                if arch == "arm" and variant == "v7":
                    if s in ("simulators", "desktop-full"):
                        # Skip since these metapackages aren't available in arm v7
                        continue
                _buildah_pull(full_name, dry_run)
                _print_pkg_version(full_name, package, arch, variant, args.dry_run)
    else:
        # ROS 2
        suffixes = [
            "ros-core",
            "ros-base",
            "desktop",
            "perception",
            "simulation",
            "desktop-full",
        ]
        architectures = [
            ("amd64", None),
            ("arm64", "v8"),
        ]
        for s in suffixes:
            tag = f"{ros_distro}-{s}"
            package = f"ros-{ros_distro}-{s}"
            full_name = _full_name(args.registry, args.name, tag)
            for arch, variant in architectures:
                _buildah_pull(full_name, dry_run)
                _print_pkg_version(full_name, package, arch, variant, args.dry_run)
                _print_ros2_help(full_name, arch, variant, dry_run)


if __name__ == "__main__":
    main()
