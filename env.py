import pybullet as p
import pybullet_data
from Robot import Robot
import numpy as np


class Env:

    def __init__(self, graphic=True, nb_robot=100, models=[]):

        if graphic:
            self.physicsClient = p.connect(p.GUI)
        else:
            self.physicsClient = p.connect(p.DIRECT)

        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -10)

        self.robots = []
        # assignation des positions des robots aleatoirement
        start_poses = np.random.randn(len(models), 3) * 4

        # on fixe la hauteur a 0.3
        start_poses[:, 2] = 0.3
        start_orientation = p.getQuaternionFromEuler([0, 0, 0])

        # on charge les models dans les robots
        for i in range(len(models)):
            self.robots.append(Robot(start_poses[i], start_orientation, models[i]))

        self.nb_robot = nb_robot
        self.load_robots()
        self.load_plane()
        self.load_collision()

    def load_robots(self, reset=False):
        # list des positions initiales des robots qui seront aleatoires
        start_poses = np.random.randn(self.nb_robot, 3) * 4

        # on fixe la hauteur a 0.3
        start_poses[:, 2] = 0.3
        start_orientation = p.getQuaternionFromEuler([0, 0, 0])

        if reset:
            # on reset juste la position des robots ainsi que les attribues comme la fitness, etc.
            for i in range(self.nb_robot):
                self.robots[i].reset()
                p.resetBasePositionAndOrientation(
                    self.robots[i].robotId, start_poses[i], start_orientation)

        elif not reset:  # on rajoute les robots dans la simulation
            for i in range(self.nb_robot - len(self.robots)):
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
        # chargement du plateau
        self.planeId = p.loadURDF("plane.urdf")

    def load_genes(self, list_genes):
        # chargement des genes dans les robots pour faire les predictions
        size_list_genes = len(list_genes)

        for i in range(self.nb_robot):
            robot = self.robots[i]

            if size_list_genes < 1:
                robot.model.set_weights([])
            else:
                robot.model.set_weights(list_genes[i])

    def computeGeneration(self, length_gen):
        for i in range(length_gen):
            if self.step() < 1:  # tourne tant qu'il y a des robots en vie
                break

    def step(self):
        """
        Pour calculer une étape pour le moteur et l'algo
        on calcule le step de chaque robot
        Return le nombre de robots encore en vie
        """
        nb_alive = self.nb_robot

        for robot in self.robots:
            robot.step()
            if not robot.alive:
                nb_alive -= 1

        p.stepSimulation(self.physicsClient)

        return nb_alive

    def disconnect(self):
        p.disconnect()

    def reset(self):
        self.load_robots(True)
