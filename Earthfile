VERSION 0.8

IMPORT ./ros1 AS ros1
IMPORT ./ros2 AS ros2
IMPORT ./ros-dev AS ros-dev


rolling:
    ARG registry='localhost/'
    ARG image_name='ros'
    BUILD --pass-args ros2+rolling


jazzy:
    ARG registry='localhost/'
    ARG image_name='ros'
    BUILD --pass-args ros2+jazzy


humble:
    ARG registry='localhost/'
    ARG image_name='ros'
    BUILD --pass-args ros2+humble


noetic:
    ARG registry='localhost/'
    ARG image_name='ros'
    BUILD --pass-args ros1+noetic


ros-dev-all:
    ARG registry='localhost/'
    ARG image_name='ros-dev'
    BUILD --pass-args +ros-dev-ubuntu-noble
    BUILD --pass-args +ros-dev-ubuntu-jammy


ros-dev-ubuntu-noble:
    ARG registry='localhost/'
    ARG image_name='ros-dev'
    BUILD --pass-args ros-dev+ubuntu-noble


ros-dev-ubuntu-jammy:
    ARG registry='localhost/'
    ARG image_name='ros-dev'
    BUILD --pass-args ros-dev+ubuntu-jammy


rolling-multiarch:
    ARG registry='localhost/'
    ARG image_name='ros'
    BUILD --pass-args --platform=linux/amd64 --platform=linux/arm64/v8 +rolling


jazzy-multiarch:
    ARG registry='localhost/'
    ARG image_name='ros'
    BUILD --pass-args --platform=linux/amd64 --platform=linux/arm64/v8 +jazzy


humble-multiarch:
    ARG registry='localhost/'
    ARG image_name='ros'
    BUILD --pass-args --platform=linux/amd64 --platform=linux/arm64/v8 +humble


noetic-multiarch:
    ARG registry='localhost/'
    ARG image_name='ros'
    BUILD --pass-args --platform=linux/amd64 --platform=linux/arm/v7 --platform=linux/arm64/v8 +noetic


ros-dev-all-multiarch:
    ARG registry='localhost/'
    ARG image_name='ros-dev'
    BUILD --pass-args +ros-dev-ubuntu-noble-multiarch
    BUILD --pass-args +ros-dev-ubuntu-jammy-multiarch


ros-dev-ubuntu-noble-multiarch:
    ARG registry='localhost/'
    ARG image_name='ros-dev'
    BUILD --pass-args --platform=linux/amd64 --platform=linux/arm/v7 --platform=linux/arm64/v8 +ros-dev-ubuntu-noble


ros-dev-ubuntu-jammy-multiarch:
    ARG registry='localhost/'
    ARG image_name='ros-dev'
    BUILD --pass-args --platform=linux/amd64 --platform=linux/arm/v7 --platform=linux/arm64/v8 +ros-dev-ubuntu-jammy
