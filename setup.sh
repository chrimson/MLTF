#/bin/sh
export DEBIAN_FRONTEND=noninteractive

sudo apt update -y
sudo apt upgrade -y
sudo apt install -y python3-pip python3.10-venv
sudo apt install -y unzip zip
sudo apt install -y jupyter

jupyter notebook --generate-config
sed -i "s/App\.allow_origin = ''/App.allow_origin = '*'/g" ~/.jupyter/jupyter_notebook_config.py
sed -i "s/App\.ip = 'localhost'/App.ip = '0.0.0.0'/g" ~/.jupyter/jupyter_notebook_config.py
