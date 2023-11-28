#!/bin/sh

wget -P scaaml/scaaml_intro https://storage.googleapis.com/scaaml-public/scaaml_intro/datasets.zip
wget -P scaaml/scaaml_intro https://storage.googleapis.com/scaaml-public/scaaml_intro/models.zip
unzip scaaml/scaaml_intro/datasets.zip -d scaaml/scaaml_intro
unzip scaaml/scaaml_intro/models.zip -d scaaml/scaaml_intro

python3 -m venv scaaml_env
. scaaml_env/bin/activate

cd scaaml
pip install -U pip
pip install ipykernel
python -m ipykernel install --user

pip install --require-hashes -r base-tooling-requirements.txt
pip-compile --allow-unsafe requirements.in --generate-hashes --upgrade
python3 -m pip install --require-hashes -r requirements.txt
python setup.py develop

jupyter notebook
