
import os
import sys

from gen_algo import *

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

if __name__ == "__main__":
    argv1 = False
    argv2 = 100
    argv3 = False

    if sys.argv[1]:
    	argv1 = (sys.argv[1] == 'True')

    if sys.argv[2]:
        argv2 = int(sys.argv[2])

    if sys.argv[3]:
    	argv3 = (sys.argv[3] == 'True')

    gen_algo = Gen_algo(graphic=argv1, nb_start_pop=argv2, load=argv3)
    gen_algo.start()
    gen_algo.end_algo()
