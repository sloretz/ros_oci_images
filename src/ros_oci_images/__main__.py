#!/usr/bin/env python3

import argparse
import sys

from . import ros1
from . import ros2

ARCHITECTURES = (
    "amd64",
    "arm/v7",
    "arm64/v8",
)

ROS_DISTROS = (
    ("noetic", "ubuntu:focal"),
    ("humble", "ubuntu:jammy"),
    ("iron", "ubuntu:jammy"),
    ("rolling", "ubuntu:jammy"),
)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", default="localhost", type=str)
    parser.add_argument("--name", default="ros_oci_images", type=str)
    parser.add_argument("--rosdistro", required=True, type=str)
    parser.add_argument("--architectures", default=[], action="append")
    parser.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()

    if args.rosdistro.lower() not in [d[0] for d in ROS_DISTROS]:
        sys.stderr.write(f"Unsupported ROS DISTRO: {args.rosdistro}\n")
        sys.exit(1)

    for arch in args.architectures:
        if arch not in ARCHITECTURES:
            sys.stderr.write(f"Unsupported arch {args.architectures}\n")
            sys.exit(1)

    if not args.architectures:
        args.architectures = ARCHITECTURES

    return args


def main():
    args = parse_arguments()

    rosdistro = args.rosdistro.lower()

    for d, base_image in ROS_DISTROS:
        if d == rosdistro:
            break

    if "noetic" == rosdistro:
        ros1.build_images(
            registry=args.registry,
            name=args.name,
            rosdistro=rosdistro,
            base_image=base_image,
            architectures=args.architectures,
            dry_run=args.dry_run,
        )
    else:
        ros2.build_images(
            registry=args.registry,
            name=args.name,
            rosdistro=rosdistro,
            base_image=base_image,
            architectures=args.architectures,
            dry_run=args.dry_run,
        )


if __name__ == "__main__":
    main()
