import pybullet as p
import pybullet_data
import time
from robot import Robot


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
        start_orientation = p.getQuaternionFromEuler([0, 0, 0])

        # On instancie nos robots mais pour
        # l'instant ils ont tous la même position
        for i in range(self.nb_robot):
            self.robots[i] = Robot(start_pos, start_orientation)

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
        for i in range(self.nb_robot):
            self.robots.step(num)

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
