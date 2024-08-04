VERSION 0.8

IMPORT ./ros1 AS ros1
IMPORT ./ros2 AS ros2


rolling:
    ARG registry='localhost/'
    ARG image_name='ros'
    BUILD --pass-args ros2+rolling


jazzy:
    ARG registry='localhost/'
    ARG image_name='ros'
    BUILD --pass-args ros2+jazzy


iron:
    ARG registry='localhost/'
    ARG image_name='ros'
    BUILD --pass-args ros2+iron


humble:
    ARG registry='localhost/'
    ARG image_name='ros'
    BUILD --pass-args ros2+humble


noetic:
    ARG registry='localhost/'
    ARG image_name='ros'
    BUILD --pass-args ros1+noetic


rolling-multiarch:
    ARG registry='localhost/'
    ARG image_name='ros'
    BUILD --pass-args --platform=linux/amd64 --platform=linux/arm64/v8 +rolling


jazzy-multiarch:
    ARG registry='localhost/'
    ARG image_name='ros'
    BUILD --pass-args --platform=linux/amd64 --platform=linux/arm64/v8 +jazzy


iron-multiarch:
    ARG registry='localhost/'
    ARG image_name='ros'
    BUILD --pass-args --platform=linux/amd64 --platform=linux/arm64/v8 +iron


humble-multiarch:
    ARG registry='localhost/'
    ARG image_name='ros'
    BUILD --pass-args --platform=linux/amd64 --platform=linux/arm64/v8 +humble


noetic-multiarch:
    ARG registry='localhost/'
    ARG image_name='ros'
    BUILD --pass-args --platform=linux/amd64 --platform=linux/arm/v7 --platform=linux/arm64/v8 +noetic
