#!/bin/bash

# Update the package index and install essential dependencies
sudo apt update
sudo apt install -y curl wget build-essential libssl-dev libffi-dev python3-dev

# Install the latest version of Python and pip
sudo apt install -y python3 python3-pip
sudo -H pip3 install --upgrade pip

# Install Python development tools and virtual environment
sudo apt install -y python3-venv python3-wheel

# Install Docker and docker-compose
sudo apt install -y docker.io
sudo usermod -aG docker $USER
sudo systemctl enable docker.service
sudo systemctl start docker.service
sudo -H pip3 install docker-compose

# Create a virtual environment and activate it
python3 -m venv env
source env/bin/activate

# Install the required packages from requirements.txt file
pip3 install -r requirements.txt

# Migrate using cookie-cutter development settings
python3 manage.py migrate --settings=cookiecutter.development
