# pylint: disable=W0312, C0111

from env import Env
import os

from gen_algo import *

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

if __name__ == "__main__":
    print(bool(sys.argv[1]))
    gen_algo = Gen_algo(graphic=sys.argv[1] == 'True', nb_start_pop=int(sys.argv[2]))
    gen_algo.start()
    gen_algo.end_algo()
