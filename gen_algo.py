# import time
import numpy as np
# import keras

from env import Env
from genetic import *


class Gen_algo:
    def __init__(self, graphic=False, nb_steps=1000, nb_start_pop=100, nb_gen=10000):
        self.nb_steps = nb_steps  # nb de move par run
        self.nb_start_pop = nb_start_pop  # nb de robot dans la pop de depart
        self.list_genes = []
        self.nb_gen = nb_gen
        self.env = Env(graphic=graphic, nb_robot=nb_start_pop)

        self.nb_boss = int(self.nb_start_pop * 0.1) if self.nb_start_pop > 10 else 10
        # *2 pour le croisement qui se fait par pair de parent
        self.nb_children_from_cross = int(self.nb_start_pop * 0.1) * 2

    def start(self):
        # boucle de generation
        for num_gen in range(1, self.nb_gen):
            print(" ")
            print("======================================================")
            print("Generation: ", num_gen)

            # keras.backend.clear_session()

            # pas besoins de load_genes la premiere fois, alors que les robots
            # ont déjà été initialisés
            if num_gen != 1:
                self.env.load_genes(self.list_genes)

            # ON FAIT JOUER CHAQUE ROBOT
            self.env.computeGeneration(self.nb_steps)

            # TRIE DES ROBOTS CROISSANT AVEC LA FITNESS
            list_robots = self.env.robots
            list_robots.sort(key=lambda x: x.computeFitness(), reverse=True)

            # Notre liste robot est triée donc list_fitness_overall aussi
            list_fitness_overall = np.array(
                [robot.computeFitness() for robot in list_robots])

            print("Moyenne des fitness: ", np.mean(list_fitness_overall))
            print("Resultat des boss: ", list_fitness_overall[:self.nb_boss])

            # SELECTION DES MEILLEURS ROBOTS
            new_list_genes = []
            
            for j in range(0, self.nb_boss):
                new_list_genes.append(list_robots[j].model.get_weights())
            

            size_genes_from_boss = len(new_list_genes)

            # POUR LES PAIRS DE BOSS(meilleurs robots)
            
            for k in range(0, size_genes_from_boss-1, 2):

                b1 = new_list_genes[k]
                b2 = new_list_genes[k+1]

                # CROISEMENT 
                list_genes_croisement = croisement(b1, b2, self.nb_children_from_cross)

                # MUTATIONS
                for gene in mutate_list(list_genes_croisement, self.nb_children_from_cross / 2, 2):
                    self.list_genes.append(gene)

            self.env.reset()

    def end_algo():
        self.env.disconnect()
