# import time
import numpy as np
import keras

from env import Env
from genetic import *

class Gen_algo:
    def __init__(self,graphic=False, nb_steps=1000, nb_start_pop=100, nb_gen=10000):
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

            # keras.backend.clear_session()

            list_fitness_overall = []
            
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

            # Selection des x meilleurs robot
            for j in range(0, 10):
                new_list_genes.append(list_robots[j].genes)
                list_fitness.append(list_robots[j].computeFitness())

            print("resultat des boss: ", list_fitness)

            size_genes_from_boss = len(new_list_genes)

            # Croisement

            for k in range(0, size_genes_from_boss-1):

                b1 = new_list_genes[k]
                b2 = new_list_genes[k+1]

                list_genes_croisement = croisement(b1, b2, 10)

                for gene in mutate_list(list_genes_croisement, 6, 2):
                    self.list_genes.append(gene)
                    
            self.env.reset()
    def end_algo():
        self.env.disconnect()
