import pybullet as p
import pybullet_data
import time
from Robot import Robot
import numpy as np
from genetic import *
import keras


class Env:

    def __init__(self, graphic=True,nb_robot=100):

        if graphic:
            self.physicsClient = p.connect(p.GUI)
        else:
            self.physicsClient = p.connect(p.DIRECT)

        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -10)

        # Init
        self.nb_robot = nb_robot
        self.robots = []
        self.load_robots()
        self.load_plane()

    def load_robots(self, list_genes=[]):
        # list des positions initiales des robots qui seront aleatoires
        start_poses = np.random.randn(self.nb_robot, 3) * 3
        # on fixe la hauteur a 1
        start_poses[:,2] = 1
        start_orientation = p.getQuaternionFromEuler([0.1, 0, 0])

        # On instancie nos robots mais pour
        # l'instant ils ont tous la même position
        for i in range(self.nb_robot):
            self.robots.append(Robot(start_poses[i], start_orientation))

        # Quand la génération est finie, on peut appeler computeFitness pour chaque robot

    def load_plane(self):
        self.planeId = p.loadURDF("plane.urdf")

    def load_genes(self, list_genes):
        for i in range(self.nb_robot):
            robot = self.robots[i]
            if len(list_genes) < 1:
                genes = []
            else:
                genes = list_genes[i]
            robot.genes = genes
            robot.model = gen_NN(genes)

    def computeGeneration(self, length_gen):
        for i in range(length_gen):
            if self.step() < 1:
                break


    def step(self):
        """
        Pour calculer une étape pour le moteur et l'algo
        on calcule le step de chaque robot
        """
        nb_alive = self.nb_robot

        for robot in self.robots:
            robot.step()
            if not robot.alive:
                nb_alive -= 1

        p.stepSimulation(self.physicsClient)
        #time.sleep(1. / 20000.)

        return nb_alive

    def save(self):
        """
                Save le résultat
                :return: jesaispas
                """
        pass

    def disconnect(self):
        p.disconnect()

    def reset(self):
        start_poses = np.random.randn(self.nb_robot, 3) * 3
        start_poses[:,2] = 1
        start_orientation = p.getQuaternionFromEuler([0.1, 0, 0])
        for i in range(self.nb_robot):
            robot = self.robots[i]
            robot.reset()
            p.resetBasePositionAndOrientation(robot.robotId, start_poses[i], start_orientation)
