from tkinter import *
# import gc
# import time
import numpy as np
# import math
# from math import hypot
import random
# import pandas as pd
# from tqdm import tqdm
from keras.models import Model
from keras.layers import Dense, Input, Flatten, Conv2D, MaxPooling2D
"""
import keras.backend as K
import tensorflow
from pynput.keyboard import Key, Controller, Listener
import copy
from multiprocessing.dummy import Pool as ThreadPool
from concurrent.futures import ThreadPoolExecutor
from tensorflow.python.client import device_lib
"""

# import os


def gen_NN(genes=[]):
    # Inputs
    input = Input(shape=(2,))

    x = Dense(60, activation='relu')(input)
    x = Dense(40, activation='relu')(x)
    predictions = Dense(1, activation='relu')(x)

    model = Model(inputs=input, outputs=predictions)

    if len(genes) > 0:
        model.set_weights(genes)
    model._make_predict_function()

    return model


def croisement(w1, w2, nb_enfants):
    """
    b1.fitness > b2.fitness
    renvoie le croisement entre les poids des 2 parents
    c'est a dire 2 enfants avec des poids qui seront un mixte des parents
    """
    list_enfants = []

    for i in range(0, nb_enfants):
        # nombre aleatoire compris entre - 0.5 et 1.5
        # utiliser pour faire le croisement
        p = random.uniform(-0.5, 1.5)

        # poids du nouvel enfant
        e = np.multiply(p, w1) + np.multiply(w2, (1 - p))

        list_enfants.append(e)
    return list_enfants


def mutate(genes, nb, coeff):
    for k in range(0, len(genes)):
        # on skip les couches qui qui n'ont pas de poids
        if len(genes[k].shape) > 1 and random.randint(0, nb == 0):
            matrice_muta = np.random.random(genes[k].shape)
            genes[k] += np.multiply(matrice_muta - 0.5, coeff)


def mutate_list(list_bot, nb, coeff):
    l = len(list_bot)
    for i in range(0, l):
        mutate(list_bot[i], max(0, nb - (l - i)), coeff)

    return list_bot
