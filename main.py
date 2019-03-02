# pylint: disable=W0312, C0111

from env import Env
import os

from gen_algo import *

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

if __name__ == "__main__":
    gen_algo = Gen_algo(graphic=False, nb_start_pop=10)
    gen_algo.start()
    gen_algo.end_algo()
