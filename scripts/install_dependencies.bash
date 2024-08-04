#!/bin/bash
set -eu -o pipefail

# Install qemu-user-static
sudo apt-get update && sudo apt-get install -y qemu-user-static
