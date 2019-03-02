import pybullet as p
import pybullet_data
import time
from Robot import Robot
import numpy as np
import genetic
import keras

from env import Env
from genetic import *

class Gen_algo:
    def __init__(self,graphic=False, nb_steps=1000, nb_start_pop=100, nb_gen=100):
        self.nb_steps = nb_steps  # nb de move par run
        self.nb_start_pop = nb_start_pop  # nb de robot dans la pop de depart
        self.list_genes = []
        self.nb_gen = nb_gen
        self.env = Env(graphic=graphic, nb_robot=nb_start_pop)

    def start(self):
        # boucle de generation
        for i in range(1, self.nb_gen):
            print(" ")
            print("======================================================")
            print("Generation: ", i)

            keras.backend.clear_session()

            list_fitness_overall = []
            list_lignes_overall = []
            self.env.load_genes(self.list_genes)

            # on fait jouer chaque robot
            #print("compute generation")
            self.env.computeGeneration(self.nb_steps)

            # trie des robots par ordre de fitness
            list_robots = self.env.robots
            list_robots.sort(key=lambda x: x.computeFitness(), reverse=True)
            list_fitness_overall = np.array([robot.computeFitness() for robot in list_robots])
            new_list_genes = []

            list_fitness = []
            print("moyenne des fitness: ", np.mean(list_fitness_overall))
            # selection des x meilleurs robots
            #print("selection")
            for j in range(0, 10):
                new_list_genes.append(list_robots[j].genes)
                list_fitness.append(list_robots[j].computeFitness())

            print("resultat des boss: ", list_fitness)

            list_genes = []

            l = len(new_list_genes)

            list_enfants = []

            # croisement
            #print("croisement")
            for k in range(1, l):

                b1 = new_list_genes[l - k]
                b2 = new_list_genes[l - k - 1]

                list_genes.append(b1)
                # list_genes.append(b2)

                list_croisement = croisement(b1, b2, 10)

                for gene in mutate_list(list_croisement, 6, 2):
                    self.list_genes.append(gene)
            self.env.reset()
    def end_algo():
        self.env.disconnect()
