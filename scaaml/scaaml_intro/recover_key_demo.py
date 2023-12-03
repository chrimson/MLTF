import logging
import os
import json
import numpy as np
from tqdm.auto import tqdm
from tensorflow.keras import metrics
from scaaml.aes import ap_preds_to_key_preds
from scaaml.plot import plot_trace, plot_confusion_matrix
from scaaml.utils import tf_cap_memory, from_categorical
from scaaml.model import get_models_by_attack_point, get_models_list, load_model_from_disk
from scaaml.intro.generator import list_shards, load_attack_shard
from scaaml.utils import hex_display, bytelist_to_hex

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['AUTOGRAPH_VERBOSITY'] = '0'
logging.getLogger('tensorflow').setLevel(logging.FATAL)
target = 'stm32f415_tinyaes'
tf_cap_memory()
target_config = json.loads(open("config/" + target + '.json').read())
BATCH_SIZE = target_config['batch_size']
TRACE_LEN = target_config['max_trace_len']

available_models = get_models_by_attack_point(target_config)

DATASET_GLOB = "datasets/%s/test/*" % target_config['algorithm']
shard_paths  = list_shards(DATASET_GLOB, 256)

ATTACK_POINT = 'sub_bytes_out' # let's pick an attack point- Key is not a good target: it doesn't work for TinyAEs
TARGET_SHARD = 42 # a shard == a different key. Pick the one you would like
NUM_TRACES = 5  # how many traces to use - as seen in single byte, 5 traces is enough

# perfoming 16x the byte recovery algorithm showecased above - one for each key byte
real_key = [] # what we are supposed to find
recovered_key = [] # what we predicted
pb = tqdm(total=16, desc="guessing key", unit='guesses')
for ATTACK_BYTE in range(16):
    # data
    keys, pts, x, y = load_attack_shard(shard_paths[TARGET_SHARD], ATTACK_BYTE, ATTACK_POINT, TRACE_LEN, num_traces=NUM_TRACES, full_key=True)
    real_key.append(keys[0])

    # load model
    model = load_model_from_disk(available_models[ATTACK_POINT][ATTACK_BYTE])

    # prediction
    predictions = model.predict(x)

    # computing byte prediction from intermediate predictions
    key_preds = ap_preds_to_key_preds(predictions, pts, ATTACK_POINT)

    # accumulating probabity
    vals = np.zeros((256))
    for trace_count, kp in enumerate(key_preds):
        vals = vals  + np.log10(kp + 1e-22)

    # order predictions by probability
    guess_ranks = (np.argsort(vals, )[-256:][::-1])

    # take strongest guess as our key guess
    recovered_key.append(guess_ranks[0])

    # update display
    pb.set_postfix({'Recovered key': bytelist_to_hex(recovered_key), "Real key": bytelist_to_hex(real_key)})
    pb.update()

pb.close()

# check that everything worked out: the recovered key match the real keys
hex_display(real_key, 'real key')
hex_display(recovered_key, 'recovered key')
