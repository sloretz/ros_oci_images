#!/bin/bash
set -eu -o pipefail

sudo add-apt-repository ppa:longsleep/golang-backports
sudo apt-get update
sudo apt-get install -y \
    bats \
    btrfs-progs \
    git \
    go-md2man \
    golang-1.21 \
    libapparmor-dev \
    libglib2.0-dev \
    libgpgme11-dev \
    libseccomp-dev \
    libselinux1-dev \
    make \
    skopeo

git clone https://github.com/containers/buildah -b v1.34.0
cd buildah
make runc all SECURITYTAGS="apparmor seccomp"
sudo make install install.runc
buildah --version
