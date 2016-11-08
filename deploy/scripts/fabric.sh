#!/bin/bash
header () {
    echo "--------------------------------------------------------------------------------"
    echo $1
    echo "--------------------------------------------------------------------------------"
}

APP_PATH=$(realpath $(pwd)'/../../app/')

header "Updating system"
sudo apt-get update && sudo apt-get upgrade -y

header "Install Python Fabric"
sudo apt-get install -y python-pip python-dev fabric

header "All operations have done. Usage: fab vagrant deploy_all"
