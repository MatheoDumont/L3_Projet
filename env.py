import pybullet as p
import pybullet_data
import time
from Robot import Robot
import numpy as np


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

    def load_robots(self):
        start_pos = [0, 0, 1]
        start_poses = np.random.randn(self.nb_robot, 3) * 4
        start_poses[:,2] = 1
        #print(start_poses)
        start_orientation = p.getQuaternionFromEuler([0, 0, 0])

        # On instancie nos robots mais pour
        # l'instant ils ont tous la même position
        for i in range(self.nb_robot):
            self.robots.append(Robot(start_poses[i], start_orientation))

        # Quand la génération est finie, on peut appeler computeFitness pour chaque robot

    def load_plane(self):
        self.planeId = p.loadURDF("plane.urdf")


    def computeGeneration(self, length_gen):

        for i in range(1,length_gen):
            self.step(i)

    def step(self, num):
        """
        Pour calculer une étape pour le moteur et l'algo
        on calcule le step de chaque robot
        """
        for robot in self.robots:
            robot.step(num)

        p.stepSimulation(self.physicsClient)
        time.sleep(1. / 200.)

    def save(self):
        """
                Save le résultat
                :return: jesaispas
                """
        pass

    def disconnect(self):
        p.disconnect()
