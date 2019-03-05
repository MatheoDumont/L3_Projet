# from tkinter import *
# import gc
# import time
import numpy as np
# import math
# from math import hypot
import random
# import pandas as pd
# from tqdm import tqdm
from keras.models import Model
from keras.layers import Dense, Input
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
    input = Input(shape=(6,))

    x = Dense(10, activation='tanh')(input)
    x = Dense(10, activation='tanh')(x)

    predictions = Dense(1, activation='tanh')(x)

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
    list_genes_children = []

    for i in range(0, nb_enfants):
        # nombre aleatoire compris entre - 0.5 et 1.5
        # utiliser pour faire le croisement
        p = random.uniform(-0.5, 1.5)

        # poids du nouvel enfant
        e = np.multiply(p, w1) + np.multiply(w2, (1 - p))

        list_genes_children.append(e)
    return list_genes_children


def mutate(genes, nb, coeff):
    for k in range(0, len(genes)):
        
        # on skip les couches qui qui n'ont pas de poids
        # ou celles qu'on ne veut pas muter pour les garder 
        # telles qu'elles sont

        if len(genes[k].shape) > 1 and random.randint(0, nb) == 0:

            matrice_muta = np.random.random(genes[k].shape)

            genes[k] += np.multiply(matrice_muta - 0.5, coeff)


def mutate_list(list_genes, nb, coeff): 

    size_list_genes = len(list_genes)

    # En fonction de nb, les plus ou mois premiers genes reçus ne seront pas mutés
    # si n est égale à la moitié de size_list_genes donc à la moitié des genes donnés à mutés
    # seulement la seconde partie sera muté

    for i in range(0, size_list_genes):
        mutate(list_genes[i], max(0, nb - (size_list_genes - i)), coeff)

    return list_genes
