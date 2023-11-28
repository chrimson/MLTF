#!/bin/sh

export DEBIAN_FRONTEND=noninteractive
sudo sed -i "s/#\$nrconf{kernelhints} = -1;/\$nrconf{kernelhints} = -1;/g" /etc/needrestart/needrestart.conf
sudo sed -i "s/#\$nrconf{restart} = 'i';/\$nrconf{restart} = 'a';/g" /etc/needrestart/needrestart.conf

sudo apt update -y
sudo apt upgrade -y
sudo apt install -y python3-pip python3.10-venv
sudo apt install -y unzip zip
sudo apt install -y jupyter

jupyter notebook --generate-config
sed -i "s/# c.NotebookApp\.allow_origin = ''/c.NotebookApp.allow_origin = '*'/g" ~/.jupyter/jupyter_notebook_config.py
sed -i "s/# c.NotebookApp\.ip = 'localhost'/c.NotebookApp.ip = '0.0.0.0'/g" ~/.jupyter/jupyter_notebook_config.py
