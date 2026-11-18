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
import json
import subprocess


def _full_name(registry, name, tag):
    return f"{registry}/{name}:{tag}"


def _bake_targets(ros_distro):
    output = subprocess.check_output(
        ["docker", "buildx", "bake", "--print", ros_distro],
        text=True,
    )
    definition = json.loads(output)
    combos = []
    for target_cfg in definition["target"].values():
        variant = target_cfg["target"]
        for platform in target_cfg["platforms"]:
            combos.append((variant, platform))
    return combos


def _pull(full_name, dry_run):
    cmd = ["docker", "pull", full_name]
    if dry_run:
        print(cmd)
    else:
        subprocess.check_call(cmd)


def _run(full_name, extra_cmd, platform=None, dry_run=False):
    cmd = ["docker", "run", "--rm=true"]
    if platform:
        cmd.append("--platform")
        cmd.append(platform)
    cmd.append(full_name)
    cmd.extend(extra_cmd)
    if dry_run:
        print(cmd)
    else:
        subprocess.check_call(cmd)


def _print_ros2_help(full_name, platform=None, dry_run=False):
    cmd = ["ros2", "--help"]
    _run(full_name, cmd, platform, dry_run)


def _print_pkg_version(full_name, pkg, platform=None, dry_run=False):
    cmd = ["apt-cache", "show", pkg]
    _run(full_name, cmd, platform, dry_run)


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

    for image, platform in _bake_targets(ros_distro):
        tag = f"{ros_distro}-{image}"
        package = f"ros-{ros_distro}-{image}"
        full_name = _full_name(args.registry, args.name, tag)
        _pull(full_name, dry_run)
        _print_pkg_version(full_name, package, platform, dry_run)
        _print_ros2_help(full_name, platform, dry_run)


if __name__ == "__main__":
    main()
