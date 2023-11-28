#!/bin/sh

python3 -m venv tf
source tf/bin/activate

pip install -U pip
pip install -U tensorflow-cpu
pip install ipykernel
python -m ipykernel install --user

python3 -c "import tensorflow as tf; print(tf.reduce_sum(tf.random.normal([1000, 1000])))"

jupyter notebook
