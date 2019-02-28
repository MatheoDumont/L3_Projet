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
        cubeStartPos = [0, 0, 1]
        cubeStartOrientation = p.getQuaternionFromEuler([0, 0, 0])

        # On instancie nos robots mais pour
        # l'instant ils ont tous la même position
        for i in range(self.nb_robot):
            self.robots[i] = Robot(cubeStartPos, cubeStartOrientation)

    def load_plane(self):
        self.planeId = p.loadURDF("plane.urdf")

    def step(self):
        """
        Pour calculer une étape pour le moteur et l'algo
        on calcule le step de chaque robot
        """
        for i in range(self.nb_robot):
            self.robots.step()

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
