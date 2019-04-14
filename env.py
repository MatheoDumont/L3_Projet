import pybullet as p
import pybullet_data
# import time
from Robot import Robot
import numpy as np

# import keras


class Env:

    def __init__(self, graphic=True, nb_robot=100, models=[]):

        if graphic:
            self.physicsClient = p.connect(p.GUI)
        else:
            self.physicsClient = p.connect(p.DIRECT)

        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -10)

        if graphic:
            pass
            # on enleve le timestep car cela fausse les mesures
            # et fais mal fonctionner les robots
            # p.setTimeStep(0.01)

        # Init

        self.robots = []
        start_poses = np.random.randn(len(models), 3) * 3
        # on fixe la hauteur a 0.3
        start_poses[:, 2] = 0.3
        start_orientation = p.getQuaternionFromEuler([0.1, 0, 0])
        # on charge les models dans les robots
        for i in range(len(models)):
            self.robots.append(Robot(start_poses[i], start_orientation, models[i]))

        self.nb_robot = nb_robot
        self.load_robots()
        self.load_plane()
        self.load_collision()

    def load_robots(self, reset=False):
        # list des positions initiales des robots qui seront aleatoires
        start_poses = np.random.randn(self.nb_robot, 3) * 3

        # on fixe la hauteur a 0.3
        start_poses[:, 2] = 0.3
        start_orientation = p.getQuaternionFromEuler([0.1, 0, 0])

        if reset:
            for i in range(self.nb_robot):
                self.robots[i].reset()
                p.resetBasePositionAndOrientation(
                    self.robots[i].robotId, start_poses[i], start_orientation)

        elif not reset:
            for i in range(self.nb_robot):
                self.robots.append(Robot(start_poses[i], start_orientation))

    def load_collision(self):
        # Doit être appelé après avoir générer les robots et le plateau
        for i in range(0, len(self.robots)):
            # On désactive les collisions entre les robots,
            # en pratique chaque robot a son propore groupe et mask
            # avec i, donc aucun ne peuvent avoir de collision entre eux
            p.setCollisionFilterGroupMask(self.robots[i].robotId, -1, i, i)

            # On rend la collision possible avec le sol
            p.setCollisionFilterPair(
                self.robots[i].robotId, self.planeId, -1, -1, 1)

    def load_plane(self):
        self.planeId = p.loadURDF("plane.urdf")

    def load_genes(self, list_genes):
        size_list_genes = len(list_genes)

        for i in range(self.nb_robot):
            robot = self.robots[i]

            if size_list_genes < 1:
                robot.model.set_weights([])
            else: 
                #print(len(list_genes[i]))
                robot.model.set_weights(list_genes[i])

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
        self.load_robots(True)
