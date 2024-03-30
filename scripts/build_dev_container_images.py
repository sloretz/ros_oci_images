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

_SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
# I'm too lazy to make a real python package
sys.path.append(_SCRIPT_DIR)
import common


SUPPORTED_OSES = {
    "ubuntu": ("jammy", ),
}


def _os_path(rel):
    """Given a name like "ubuntu", return the absolute path to the folder with a Dockerfile."""
    p = Path(_SCRIPT_DIR).parent
    return str(p.joinpath("ros-devcontainer").joinpath(rel).absolute())


def _tag(os, codename, arch, variant):
    tag = f"{os}-{codename}"
    if arch:
        tag += "-" + arch
        if variant:
            tag += "-" + variant
    return tag


def get_base_image(linux_distro, linux_code_name):
    """A place to hard code docker images to use as the base image."""

    if "ubuntu" == linux_distro.lower():
        ubuntu_base_images = {
            "focal": "ubuntu:focal",
            "20.04": "ubuntu:focal",
            "jammy": "ubuntu:jammy",
            "22.04": "ubuntu:jammy",
            "noble": "ubuntu:noble",
            "24.04": "ubuntu:noble",
        }
        if linux_code_name.lower() in ubuntu_base_images:
            return ubuntu_base_images[linux_code_name.lower()]
    raise RuntimeError(f"Unknown linux distro {linux_distro} {linux_code_name}")


@common.retry_with_backoff
def build_dev_container(
    os, codename, registry, name, arch, variant, skip_if_exists, push, dry_run
):
    pass
    # Given a name like "ubuntu"m return the absolute path to the folder with a Dockerfile
    path = _os_path(os)

    # Get base image
    base_image = get_base_image(os, codename)

    # Make a tag like ubuntu-jammy-arm64-v8
    tag = _tag(os, codename, arch, variant)

    # Make a name like ghcr.io/sloretz/ros-dev-container:ubuntu-jammy-arm64-v8
    full_name = common._full_name(registry, name, tag)

    if skip_if_exists and common._image_exists(full_name):
        return full_name

    print("IMAGE", full_name)

    cmd = [
        "buildah",
        "bud",
        "--pull=false",
        "-t",
        full_name,
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
        common._buildah_push_image(full_name, dry_run)

    return full_name


def create_manifest(os, codename, registry, name, images, push, dry_run):
    common._buildah_manifest(registry, name, f"{os}-{codename}", images, push, dry_run)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", default="localhost", type=str)
    parser.add_argument("--name", default="ros", type=str)
    parser.add_argument("--push", action="store_true")
    parser.add_argument("--skip-if-exists", action="store_true")
    parser.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()
    dry_run = args.dry_run

    for os, codenames in SUPPORTED_OSES.items():
        assert os.lower() == os
        for codename in codenames:
            assert codename.lower() == codename
            amd64_image = build_dev_container(
                os,
                codename,
                args.registry,
                args.name,
                "amd64",
                None,
                args.skip_if_exists,
                args.push,
                dry_run,
            )
            arm_v7_image = build_dev_container(
                os,
                codename,
                args.registry,
                args.name,
                "arm",
                "v7",
                args.skip_if_exists,
                args.push,
                dry_run,
            )
            arm64_v8_image = build_dev_container(
                os,
                codename,
                args.registry,
                args.name,
                "arm64",
                "v8",
                args.skip_if_exists,
                args.push,
                dry_run,
            )
            create_manifest(
                os,
                codename,
                args.registry,
                args.name,
                (amd64_image, arm_v7_image, arm64_v8_image),
                args.push,
                dry_run,
            )


if __name__ == "__main__":
    main()
