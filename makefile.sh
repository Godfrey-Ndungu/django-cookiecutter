# Define variables
PYTHON = python3
PIP = pip3
VENV = venv
SETTINGS = cookiecutter.development

# Check if Docker is installed
HAS_DOCKER := $(shell command -v docker 2> /dev/null)

# Check if Redis is installed
HAS_REDIS := $(shell command -v redis-server 2> /dev/null)

# Check if Ansible is installed
HAS_ANSIBLE := $(shell command -v ansible 2> /dev/null)

# Install dependencies
deps:
ifeq ($(HAS_DOCKER),)
    sudo apt update && sudo apt install -y curl wget build-essential libssl-dev libffi-dev python3-dev python3 python3-pip python3-venv python3-wheel docker.io
    sudo usermod -aG docker $USER
    sudo systemctl enable docker.service
    sudo systemctl start docker.service
    sudo -H pip3 install --upgrade pip docker-compose
else
    sudo apt update && sudo apt install -y curl wget build-essential libssl-dev libffi-dev python3-dev python3 python3-pip python3-venv python3-wheel
    sudo -H pip3 install --upgrade pip
    sudo -H pip3 install docker-compose
endif
ifeq ($(HAS_ANSIBLE),)
    sudo apt-get update && sudo apt-get install -y software-properties-common
    sudo apt-add-repository -y ppa:ansible/ansible
    sudo apt-get update && sudo apt-get install -y ansible
endif
ifeq ($(HAS_REDIS),)
    sudo apt update && sudo apt install -y redis
    sudo redis-server
endif

# Create virtual environment and install required packages
install:
    $(PYTHON) -m venv $(VENV)
    source $(VENV)/bin/activate && $(PIP) install -r requirements.txt
    $(PYTHON) manage.py migrate --settings=$(SETTINGS)

# Clean docs/source directory except core folder
clean:
    find docs/source -type f \( ! -path 'docs/source/core/*' -name '*.rst' \) -delete
    touch docs/source/index.rst
    touch docs/source/introduction.rst
