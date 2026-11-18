variable "REGISTRY" {
  default = "localhost"
}

variable "ROS_IMAGE_NAME" {
  default = "ros"
}

variable "ROS_DEV_IMAGE_NAME" {
  default = "ros-dev"
}

variable "DATE" {
  default = formatdate("YYYY-MM-DD", timestamp())
}

variable "TAG_SUFFIX" {
  # Optional suffix (e.g. "-amd64", "-arm64") when pushing arch-specific
  # images before combining with `docker buildx imagetools create`.
  default = ""
}

variable "USE_TESTING_REPO" {
  default = "false"
}

group "default" {
  targets = ["ros2", "ros-dev"]
}

group "rolling" {
  targets = [
    "rolling-ros-core",
    "rolling-ros-base",
    "rolling-desktop",
    "rolling-perception",
    "rolling-simulation",
    "rolling-desktop-full",
  ]
}

group "lyrical" {
  targets = [
    "lyrical-ros-core",
    "lyrical-ros-base",
    "lyrical-desktop",
    "lyrical-perception",
    "lyrical-simulation",
    "lyrical-desktop-full",
  ]
}

group "kilted" {
  targets = [
    "kilted-ros-core",
    "kilted-ros-base",
    "kilted-desktop",
    "kilted-perception",
    "kilted-simulation",
    "kilted-desktop-full",
  ]
}

group "jazzy" {
  targets = [
    "jazzy-ros-core",
    "jazzy-ros-base",
    "jazzy-desktop",
    "jazzy-perception",
    "jazzy-simulation",
    "jazzy-desktop-full",
  ]
}

group "humble" {
  targets = [
    "humble-ros-core",
    "humble-ros-base",
    "humble-desktop",
    "humble-perception",
    "humble-simulation",
    "humble-desktop-full",
  ]
}

target "ros2" {
  name = "${distro.name}-${variant}"
  matrix = {
    distro = [
      { name = "rolling", ubuntu = "ubuntu:resolute" },
      { name = "lyrical", ubuntu = "ubuntu:resolute" },
      { name = "kilted", ubuntu = "ubuntu:noble" },
      { name = "jazzy", ubuntu = "ubuntu:noble" },
      { name = "humble", ubuntu = "ubuntu:jammy" },
    ]
    variant = [
      "ros-core",
      "ros-base",
      "desktop",
      "perception",
      "simulation",
      "desktop-full",
    ]
  }
  context    = "./ros2"
  dockerfile = "Dockerfile"
  target     = variant
  args = {
    ROS_DISTRO       = distro.name
    UBUNTU_IMAGE     = distro.ubuntu
    use_testing_repo = USE_TESTING_REPO
  }
  tags = [
    "${REGISTRY}/${ROS_IMAGE_NAME}:${distro.name}-${variant}${TAG_SUFFIX}",
    "${REGISTRY}/${ROS_IMAGE_NAME}:${distro.name}-${variant}-${DATE}${TAG_SUFFIX}",
  ]
  platforms = ["linux/amd64", "linux/arm64/v8"]
}

target "ros-dev" {
  name = "ros-dev-ubuntu-${ubuntu}"
  matrix = {
    ubuntu = ["resolute", "noble", "jammy"]
  }
  context    = "./ros-dev"
  dockerfile = "Dockerfile"
  args = {
    UBUNTU_IMAGE = "ubuntu:${ubuntu}"
  }
  tags = [
    "${REGISTRY}/${ROS_DEV_IMAGE_NAME}:ubuntu-${ubuntu}${TAG_SUFFIX}",
    "${REGISTRY}/${ROS_DEV_IMAGE_NAME}:ubuntu-${ubuntu}-${DATE}${TAG_SUFFIX}",
  ]
  platforms = ["linux/amd64", "linux/arm/v7", "linux/arm64/v8"]
}
