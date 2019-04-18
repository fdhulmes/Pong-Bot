'''
datasets.py

An access point for reading in datasets.
'''

import data_collect
import projdirs
import os

def load(name):
    if (name == 'up-only'):
        dataset = data_collect.deserialize_data(os.path.join(projdirs.data_special, "up-only.dat"))
    elif (name == 'down-only'):
        dataset = data_collect.deserialize_data(os.path.join(projdirs.data_special, "down-only.dat"))
    elif (name == 'no-move'):
        dataset = data_collect.deserialize_data(os.path.join(projdirs.data_special, "no-move.dat"))
    elif (name == 'all'):
        dataset = data_collect.deserialize_all_data(projdirs.data)
    elif (name == 'ideal'):
        dataset = data_collect.deserialize_all_data(projdirs.data_special_ideal)
    return dataset