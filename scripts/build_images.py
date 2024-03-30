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
import os
from pathlib import Path
import subprocess
import sys
import time

_SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


def _full_name(registry, name, tag):
    return f"{registry}/{name}:{tag}"


def _path(rel):
    p = Path(_SCRIPT_DIR).parent
    return str(p.joinpath(rel).absolute())


def _tag(ros_distro, pkg, arch, variant):
    tag = f"{ros_distro}-{pkg}"
    if arch:
        tag += "-" + arch
        if variant:
            tag += "-" + variant
    return tag


def retry_with_backoff(func):
    def new_func(*args, **kwargs):
        for i in range(5):
            try:
                return func(*args, **kwargs)
            except subprocess.CalledProcessError:
                print("Hmm command failed, retrying in case it's network related")
                time.sleep(i * i * 15)
        raise RuntimeError("Unable to build image")

    return new_func


def _image_exists(full_name):
    cmd = ["buildah", "inspect", full_name]
    ret = subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return 0 == ret


@retry_with_backoff
def _buildah_ros_image(
    base_image,
    repo_path,
    ros_distro,
    *,
    registry,
    name,
    arch,
    variant,
    skip_if_exists,
    push,
    dry_run,
):
    # Given a path like "ros1/ros-core"
    # return the absolute path to ros1/ros-core in this repo
    path = _path(repo_path)

    # Given ros1/ros-core, the pkg name is ros-core
    pkg = Path(repo_path).name

    # Make a tag like noetic-ros-core-arm64-v8
    tag = _tag(ros_distro, pkg, arch, variant)

    # Make a name like ghcr.io/sloretz/ros:noetic-ros-core-arm64-v8
    full_name = _full_name(registry, name, tag)

    if skip_if_exists and _image_exists(full_name):
        return full_name

    print("IMAGE", full_name)

    cmd = [
        "buildah",
        "bud",
        "--pull=false",
        "-t",
        full_name,
        "--build-arg",
        f"ROS_DISTRO={ros_distro}",
        "--build-arg",
        f"FROM={base_image}",
    ]
    if arch:
        cmd.append("--arch")
        cmd.append(arch)
    if variant:
        cmd.append("--variant")
        cmd.append(variant)
    if dry_run:
        print(f"cd {path} && ", cmd)
    else:
        subprocess.check_call(cmd, cwd=path)

    if push:
        # Pushing as we go reduces impact of rate limiting on github packages
        _buildah_push_image(full_name, dry_run)

    return full_name


def _buildah_manifest(registry, name, tag, image_names, push, dry_run):
    full_name = _full_name(registry, name, tag)
    print("MANIFEST", full_name)

    create_cmd = ["buildah", "manifest", "create", full_name]
    if dry_run:
        print(create_cmd)
    else:
        subprocess.check_call(create_cmd)

    for image in image_names:
        add_cmd = ["buildah", "manifest", "add", full_name, image]
        if dry_run:
            print(add_cmd)
        else:
            subprocess.check_call(add_cmd)

    if push:
        # Pushing as we go reduces impact of rate limiting on github packages
        _buildah_push_manifest(full_name, dry_run)


@retry_with_backoff
def _buildah_push_image(image_name, dry_run):
    cmd = ["buildah", "push", image_name]
    if dry_run:
        print(cmd)
    else:
        subprocess.check_call(cmd)


@retry_with_backoff
def _buildah_push_manifest(image_name, dry_run):
    cmd = ["buildah", "manifest", "push", image_name]
    if dry_run:
        print(cmd)
    else:
        subprocess.check_call(cmd)


class Ros2Images:
    def __init__(self):
        self.ros_core = None
        self.ros_base = None
        self.perception = None
        self.simulation = None
        self.desktop = None
        self.desktop_full = None


def build_ros2_images(
    ros_distro, base_image, registry, name, arch, variant, skip_if_exists, push, dry_run
):
    """Build ROS 2 images for one specific architecture."""

    common_args = {
        "ros_distro": ros_distro,
        "registry": registry,
        "name": name,
        "arch": arch,
        "variant": variant,
        "skip_if_exists": skip_if_exists,
        "push": push,
        "dry_run": dry_run,
    }

    images = Ros2Images()

    images.ros_core = _buildah_ros_image(base_image, "ros2/ros-core", **common_args)
    images.ros_base = _buildah_ros_image(
        images.ros_core, "ros2/ros-base", **common_args
    )
    images.perception = _buildah_ros_image(
        images.ros_base, "ros2/perception", **common_args
    )
    images.desktop = _buildah_ros_image(images.ros_base, "ros2/desktop", **common_args)
    if "rolling" != ros_distro:
        # TODO(https://github.com/sloretz/ros_oci_images/issues/2)
        images.desktop_full = _buildah_ros_image(
            images.desktop, "ros2/desktop-full", **common_args
        )
        images.simulation = _buildah_ros_image(
            images.ros_base, "ros2/simulation", **common_args
        )

    return images


class Ros1Images:
    def __init__(self):
        self.ros_core = None
        self.ros_base = None
        self.robot = None
        self.perception = None
        self.simulators = None
        self.viz = None
        self.desktop = None
        self.desktop_full = None


def build_ros1_images(
    ros_distro, base_image, registry, name, arch, variant, skip_if_exists, push, dry_run
):
    """Build ROS 1 images for one specific architecture."""

    common_args = {
        "ros_distro": ros_distro,
        "registry": registry,
        "name": name,
        "arch": arch,
        "variant": variant,
        "skip_if_exists": skip_if_exists,
        "push": push,
        "dry_run": dry_run,
    }

    images = Ros1Images()

    images.ros_core = _buildah_ros_image(base_image, "ros1/ros-core", **common_args)
    images.ros_base = _buildah_ros_image(
        images.ros_core, "ros1/ros-base", **common_args
    )
    images.robot = _buildah_ros_image(images.ros_base, "ros1/robot", **common_args)
    images.perception = _buildah_ros_image(
        images.ros_base, "ros1/perception", **common_args
    )
    images.viz = _buildah_ros_image(images.ros_base, "ros1/viz", **common_args)
    images.desktop = _buildah_ros_image(images.robot, "ros1/desktop", **common_args)
    if not (arch == "arm" and variant == "v7"):
        # Cannot build because this platform lacks gazebo binaries
        images.desktop_full = _buildah_ros_image(
            images.desktop, "ros1/desktop-full", **common_args
        )
        images.simulators = _buildah_ros_image(
            images.robot, "ros1/simulators", **common_args
        )

    return images


def _collect(attr, set_of_images):
    ret = []
    for images in set_of_images:
        img = getattr(images, attr)
        if img:
            ret.append(img)
    return tuple(ret)


def create_ros1_manifests(registry, name, ros_distro, set_of_images, push, dry_run):
    attrs = [
        "ros_core",
        "ros_base",
        "robot",
        "perception",
        "simulators",
        "viz",
        "desktop",
        "desktop_full",
    ]
    for attr in attrs:
        suffix = attr.replace("_", "-")
        images = _collect(attr, set_of_images)
        _buildah_manifest(
            registry, name, f"{ros_distro}-{suffix}", images, push, dry_run
        )


def create_ros2_manifests(registry, name, ros_distro, set_of_images, push, dry_run):
    attrs = [
        "ros_core",
        "ros_base",
        "perception",
        "simulation",
        "desktop",
        "desktop_full",
    ]
    for attr in attrs:
        if "rolling" != ros_distro and attr in ["desktop_full", "simulation"]:
            # TODO(https://github.com/sloretz/ros_oci_images/issues/2)
            continue
        suffix = attr.replace("_", "-")
        images = _collect(attr, set_of_images)
        _buildah_manifest(
            registry, name, f"{ros_distro}-{suffix}", images, push, dry_run
        )


ROS_DISTROS = {
    "noetic": "ubuntu:focal",
    "humble": "ubuntu:jammy",
    "iron": "ubuntu:jammy",
    "rolling": "ubuntu:noble",
}


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", default="localhost", type=str)
    parser.add_argument("--name", default="ros", type=str)
    parser.add_argument("--rosdistro", required=True, type=str)
    parser.add_argument("--push", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-if-exists", action="store_true")

    args = parser.parse_args()

    if args.rosdistro.lower() not in ROS_DISTROS:
        sys.stderr.write(f"Unsupported ROS DISTRO: {args.rosdistro}\n")
        sys.exit(1)

    return args


def main():
    args = parse_arguments()

    ros_distro = args.rosdistro.lower()
    base_image = ROS_DISTROS[ros_distro]
    dry_run = args.dry_run

    if "noetic" == ros_distro:
        amd64_images = build_ros1_images(
            ros_distro,
            base_image,
            args.registry,
            args.name,
            "amd64",
            None,
            args.skip_if_exists,
            args.push,
            dry_run,
        )
        arm_v7_images = build_ros1_images(
            ros_distro,
            base_image,
            args.registry,
            args.name,
            "arm",
            "v7",
            args.skip_if_exists,
            args.push,
            dry_run,
        )
        arm64_v8_images = build_ros1_images(
            ros_distro,
            base_image,
            args.registry,
            args.name,
            "arm64",
            "v8",
            args.skip_if_exists,
            args.push,
            dry_run,
        )
        create_ros1_manifests(
            args.registry,
            args.name,
            ros_distro,
            (amd64_images, arm_v7_images, arm64_v8_images),
            args.push,
            dry_run,
        )
    else:
        amd64_images = build_ros2_images(
            ros_distro,
            base_image,
            args.registry,
            args.name,
            "amd64",
            None,
            args.skip_if_exists,
            args.push,
            dry_run,
        )
        arm64_v8_images = build_ros2_images(
            ros_distro,
            base_image,
            args.registry,
            args.name,
            "arm64",
            "v8",
            args.skip_if_exists,
            args.push,
            dry_run,
        )
        create_ros2_manifests(
            args.registry,
            args.name,
            ros_distro,
            (amd64_images, arm64_v8_images),
            args.push,
            dry_run,
        )


if __name__ == "__main__":
    main()
