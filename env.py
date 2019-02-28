import pybullet as p
import pybullet_data
import time


class Env:

    def __init__(self, graphic=True):

        if graphic:
            self.physicsClient = p.connect(p.GUI)
        else:
            self.physicsClient = p.connect(p.DIRECT)

        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -10)

        # Init
        self.robotId = 0
        self.load_robot()
        self.load_plane()

    def load_robot(self):
        cubeStartPos = [0, 0, 1]
        cubeStartOrientation = p.getQuaternionFromEuler([0, 0, 0])

        self.robotId = p.loadURDF(
            "balance.urdf", cubeStartPos, cubeStartOrientation)
        self.left_join = 0
        self.right_join = 1

    def load_plane(self):
        self.planeId = p.loadURDF("plane.urdf")

    def step(self):
        """
                Pour calculer une étape pour le moteur et l'algo
                """
        p.stepSimulation(self.physicsClient)
        time.sleep(1. / 200.)


    def moveRobot(self, left_speed, right_speed):
        """
                Pour faire avancer le robot
                """
        pass

    def getDistanceFromGround(self):
        # x z y, le y nous indique la proximité du sol et le centre du robot
        cubePos, cubeOrn = p.getBasePositionAndOrientation(self.robotId)
        return cubePos[2]  # y, si < 0.15, on peut estimer qu'il est horizontal

    def getAngleWithGround(self):
        pass

    def save(self):
        """
                Save le résultat
                :return: jesaispas
                """
        pass

    def disconnect(self):
        p.disconnect()
