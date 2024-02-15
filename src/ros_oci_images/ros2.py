from .buildah import arch_specific_tag
from .buildah import BuildahContainer
from .buildah import BuildahManifest


def build_images(
    *, registry, name, rosdistro, base_image, architectures, dry_run=False
):
    ros_core = build_ros_core(
        registry=registry,
        name=name,
        tag=f"{rosdistro}-ros-core",
        rosdistro=rosdistro,
        base_image=base_image,
        architectures=architectures,
        dry_run=dry_run,
    )
    ros_base = build_ros_base(
        registry=registry,
        name=name,
        tag=f"{rosdistro}-ros-base",
        rosdistro=rosdistro,
        base_image=ros_core,
        architectures=architectures,
        dry_run=dry_run,
    )
    ros_desktop = build_one_package_image(
        f"ros-{rosdistro}-desktop",
        registry=registry,
        name=name,
        tag=f"{rosdistro}-desktop",
        base_image=ros_base,
        architectures=architectures,
        dry_run=dry_run,
    )
    build_one_package_image(
        f"ros-{rosdistro}-desktop-full",
        registry=registry,
        name=name,
        tag=f"{rosdistro}-desktop-full",
        base_image=ros_desktop,
        architectures=architectures,
        dry_run=dry_run,
    )
    build_one_package_image(
        f"ros-{rosdistro}-perception",
        registry=registry,
        name=name,
        tag=f"{rosdistro}-perception",
        base_image=ros_base,
        architectures=architectures,
        dry_run=dry_run,
    )
    build_one_package_image(
        f"ros-{rosdistro}-simulation",
        registry=registry,
        name=name,
        tag=f"{rosdistro}-simulation",
        base_image=ros_base,
        architectures=architectures,
        dry_run=dry_run,
    )


def build_one_package_image(
    package, *, registry, name, tag, base_image, architectures, dry_run=False
):
    # Create one manifest
    manifest = BuildahManifest(registry=registry, name=name, tag=tag, dry_run=dry_run)

    for arch in architectures:
        b = BuildahContainer(
            registry=registry,
            name=name,
            tag=arch_specific_tag(tag, arch),
            base_image=base_image,
            arch=arch,
            manifest=manifest,
            dry_run=dry_run,
        )

        # Install one package
        b.run(["apt-get", "update"])
        b.run(
            [
                "apt-get",
                "install",
                "-y",
                "--no-install-recommends",
                package,
            ]
        )

        # Cleanup unnecessary stuff
        b.run(["rm", "-rf", "/var/lib/apt/lists/*"])

        # Tag the image
        b.commit()

    return manifest.full_name


def build_ros_core(
    *, registry, name, tag, rosdistro, base_image, architectures, dry_run=False
):
    # Create one manifest
    manifest = BuildahManifest(registry=registry, name=name, tag=tag, dry_run=dry_run)

    for arch in architectures:
        b = BuildahContainer(
            registry=registry,
            name=name,
            tag=arch_specific_tag(tag, arch),
            base_image=base_image,
            arch=arch,
            manifest=manifest,
            dry_run=dry_run,
        )

        # Setup timezone
        b.run(["bash", "-c", "echo Etc/UTC > /etc/timezone"])
        b.run(["ln", "-s", "/usr/share/zoneinfo/Etc/UTC", "/etc/localtime"])
        b.run(["apt-get", "update"])
        b.run(
            [
                "apt-get",
                "install",
                "--no-install-recommends",
                "-y",
                "tzdata",
            ]
        )

        # Install packages for setting up keys and sources.
        b.run(
            [
                "apt-get",
                "install",
                "--no-install-recommends",
                "-y",
                "dirmngr",
                "gnupg2",
                "lsb-release",
            ]
        )

        # Setup keys to access ROS apt repository.
        key = "C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654"
        b.run(["mkdir", "/tmp/gnupghome"])
        b.run(
            [
                "gpg",
                "--homedir=/tmp/gnupghome",
                "--batch",
                "--keyserver",
                "keyserver.ubuntu.com",
                "--recv-keys",
                key,
            ]
        )
        b.run(["mkdir", "-p", "/usr/share/keyrings"])
        b.run(
            [
                "gpg",
                "--homedir=/tmp/gnupghome",
                "--output",
                "/usr/share/keyrings/ros2-latest-archive-keyring.gpg",
                "--batch",
                "--export",
                key,
            ]
        )
        b.run(["gpgconf", "--kill", "all"])
        b.run(["rm", "-rf", "/tmp/gnupghome"])

        # Setup apt sources.list
        b.run(
            [
                "bash",
                "-c",
                'echo "deb [ signed-by=/usr/share/keyrings/ros2-latest-archive-keyring.gpg ] http://packages.ros.org/ros2/ubuntu `lsb_release -sc` main" > /etc/apt/sources.list.d/ros2-latest.list',
            ]
        )

        # Set environment variables.
        b.config(env="LANG=C.UTF-8")
        b.config(env="LC_ALL=C.UTF-8")
        b.config(env=f"ROS_DISTRO={rosdistro}")

        # Install ROS packages
        b.run(["apt-get", "update"])
        b.run(
            [
                "apt-get",
                "install",
                "-y",
                "--no-install-recommends",
                f"ros-{rosdistro}-ros-core",
            ]
        )

        # Create entrypoint script.
        entrypoint_script = "\n".join(
            [
                "#!/bin/bash",
                "set -e",
                "",
                "# Setup ROS environment",
                "",
                f'source "/opt/ros/{rosdistro}/setup.bash" --',
                'exec "$@"',
            ]
        )
        b.run(["bash", "-c", f"echo '{entrypoint_script}' > /ros_entrypoint.sh"])
        b.run(["chmod", "+x", "/ros_entrypoint.sh"])
        b.config(entrypoint='["/ros_entrypoint.sh"]')
        b.config(cmd="/bin/bash")

        # Cleanup unnecessary stuff.
        b.run(["rm", "-rf", "/var/lib/apt/lists/*"])

        # Tag the image.
        b.commit()

    return manifest.full_name


def build_ros_base(
    *, registry, name, tag, rosdistro, base_image, architectures, dry_run=False
):
    # Create one manifest
    manifest = BuildahManifest(registry=registry, name=name, tag=tag, dry_run=dry_run)

    for arch in architectures:
        b = BuildahContainer(
            registry=registry,
            name=name,
            tag=arch_specific_tag(tag, arch),
            base_image=base_image,
            arch=arch,
            manifest=manifest,
            dry_run=dry_run,
        )

        # Install bootstrap tools
        b.run(["apt-get", "update"])
        b.run(
            [
                "apt-get",
                "install",
                "--no-install-recommends",
                "-y",
                "build-essential",
                "git",
                "python3-colcon-common-extensions",
                "python3-colcon-mixin",
                "python3-rosdep",
                "python3-vcstool",
            ]
        )

        # Bootsrap rosdep
        b.run(["rosdep", "init"])
        b.run(["rosdep", "update", "--rosdistro", rosdistro])

        # Setup colcon mixin and metadata.
        b.run(
            [
                "colcon",
                "mixin",
                "add",
                "default",
                "https://raw.githubusercontent.com/colcon/colcon-mixin-repository/master/index.yaml",
            ]
        )
        b.run(["colcon", "mixin", "update"])
        b.run(
            [
                "colcon",
                "metadata",
                "add",
                "default",
                "https://raw.githubusercontent.com/colcon/colcon-metadata-repository/master/index.yaml",
            ]
        )
        b.run(["colcon", "metadata", "update"])

        # Install ROS packages
        b.run(
            [
                "apt-get",
                "install",
                "-y",
                "--no-install-recommends",
                f"ros-{rosdistro}-ros-base",
            ]
        )

        # Cleanup unnecessary stuff
        b.run(["rm", "-rf", "/var/lib/apt/lists/*"])

        # Tag the image
        b.commit()

    return manifest.full_name
