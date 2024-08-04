VERSION 0.8

IMPORT ./ros1 AS ros1
IMPORT ./ros2 AS ros2

all:
    BUILD +rolling
    BUILD +jazzy
    BUILD +iron
    BUILD +humble
    BUILD +noetic


all-multiarch:
    BUILD +rolling-multiarch
    BUILD +jazzy-multiarch
    BUILD +iron-multiarch
    BUILD +humble-multiarch
    BUILD +noetic-multiarch


rolling:
    BUILD ros2+rolling


jazzy:
    BUILD ros2+jazzy


iron:
    BUILD ros2+iron


humble:
    BUILD ros2+humble


noetic:
    BUILD ros1+noetic


rolling-multiarch:
    BUILD --platform=linux/amd64 --platform=linux/arm64/v8 ros2+rolling


jazzy-multiarch:
    BUILD --platform=linux/amd64 --platform=linux/arm64/v8 ros2+jazzy


iron-multiarch:
    BUILD --platform=linux/amd64 --platform=linux/arm64/v8 ros2+iron


humble-multiarch:
    BUILD --platform=linux/amd64 --platform=linux/arm64/v8 ros2+humble


noetic-multiarch:
    BUILD --platform=linux/amd64 --platform=linux/arm/v7 --platform=linux/arm64/v8 ros1+noetic
