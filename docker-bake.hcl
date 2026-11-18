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

variable "VARIANTS" {
  default = [
    "ros-core",
    "ros-base",
    "desktop",
    "perception",
    "simulation",
    "desktop-full",
  ]
}

group "default" {
  targets = ["ros2", "ros-dev"]
}

group "ros2" {
  targets = ["rolling", "lyrical", "kilted", "jazzy", "humble"]
}

target "_ros2" {
  context    = "."
  dockerfile = "ros.Dockerfile"
  platforms  = ["linux/amd64", "linux/arm64/v8"]
}

target "rolling" {
  inherits = ["_ros2"]
  name     = "rolling-${variant}"
  matrix = {
    variant = VARIANTS
  }
  target = variant
  args = {
    ROS_DISTRO       = "rolling"
    UBUNTU_IMAGE     = "ubuntu:resolute"
    use_testing_repo = USE_TESTING_REPO
  }
  tags = [
    "${REGISTRY}/${ROS_IMAGE_NAME}:rolling-${variant}${TAG_SUFFIX}",
    "${REGISTRY}/${ROS_IMAGE_NAME}:rolling-${variant}-${DATE}${TAG_SUFFIX}",
  ]
}

target "lyrical" {
  inherits = ["_ros2"]
  name     = "lyrical-${variant}"
  matrix = {
    variant = VARIANTS
  }
  target = variant
  args = {
    ROS_DISTRO       = "lyrical"
    UBUNTU_IMAGE     = "ubuntu:resolute"
    use_testing_repo = USE_TESTING_REPO
  }
  tags = [
    "${REGISTRY}/${ROS_IMAGE_NAME}:lyrical-${variant}${TAG_SUFFIX}",
    "${REGISTRY}/${ROS_IMAGE_NAME}:lyrical-${variant}-${DATE}${TAG_SUFFIX}",
  ]
}

target "kilted" {
  inherits = ["_ros2"]
  name     = "kilted-${variant}"
  matrix = {
    variant = VARIANTS
  }
  target = variant
  args = {
    ROS_DISTRO       = "kilted"
    UBUNTU_IMAGE     = "ubuntu:noble"
    use_testing_repo = USE_TESTING_REPO
  }
  tags = [
    "${REGISTRY}/${ROS_IMAGE_NAME}:kilted-${variant}${TAG_SUFFIX}",
    "${REGISTRY}/${ROS_IMAGE_NAME}:kilted-${variant}-${DATE}${TAG_SUFFIX}",
  ]
}

target "jazzy" {
  inherits = ["_ros2"]
  name     = "jazzy-${variant}"
  matrix = {
    variant = VARIANTS
  }
  target = variant
  args = {
    ROS_DISTRO       = "jazzy"
    UBUNTU_IMAGE     = "ubuntu:noble"
    use_testing_repo = USE_TESTING_REPO
  }
  tags = [
    "${REGISTRY}/${ROS_IMAGE_NAME}:jazzy-${variant}${TAG_SUFFIX}",
    "${REGISTRY}/${ROS_IMAGE_NAME}:jazzy-${variant}-${DATE}${TAG_SUFFIX}",
  ]
}

target "humble" {
  inherits = ["_ros2"]
  name     = "humble-${variant}"
  matrix = {
    variant = VARIANTS
  }
  target = variant
  args = {
    ROS_DISTRO       = "humble"
    UBUNTU_IMAGE     = "ubuntu:jammy"
    use_testing_repo = USE_TESTING_REPO
  }
  tags = [
    "${REGISTRY}/${ROS_IMAGE_NAME}:humble-${variant}${TAG_SUFFIX}",
    "${REGISTRY}/${ROS_IMAGE_NAME}:humble-${variant}-${DATE}${TAG_SUFFIX}",
  ]
}

target "ros-dev" {
  name = "ros-dev-ubuntu-${ubuntu}"
  matrix = {
    ubuntu = ["resolute", "noble", "jammy"]
  }
  context    = "."
  dockerfile = "ros-dev.Dockerfile"
  args = {
    UBUNTU_IMAGE = "ubuntu:${ubuntu}"
  }
  tags = [
    "${REGISTRY}/${ROS_DEV_IMAGE_NAME}:ubuntu-${ubuntu}${TAG_SUFFIX}",
    "${REGISTRY}/${ROS_DEV_IMAGE_NAME}:ubuntu-${ubuntu}-${DATE}${TAG_SUFFIX}",
  ]
  platforms = ["linux/amd64", "linux/arm/v7", "linux/arm64/v8"]
}
