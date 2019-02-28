import pybullet as p


class Robot:

    def __init__(self, cubeStartPos, cubeStartOrientation):
        self.robotId = p.loadURDF(
            "balance.urdf", cubeStartPos, cubeStartOrientation)
        self.left_join = 0
        self.right_join = 1

    def moveRobot(self, left_speed, right_speed):
        """
                Pour faire avancer le robot
                """
        p.setJointMotorControl2(
            bodyUniqueId=self.robotId,
            jointIndex=self.left_join,
            controlMode=p.VELOCITY_CONTROL,
            targetVelocity=-left_speed
        )
        p.setJointMotorControl2(
            bodyUniqueId=self.robotId,
            jointIndex=self.right_join,
            controlMode=p.VELOCITY_CONTROL,
            targetVelocity=right_speed
        )

    def step(self):
        pass

    def getDistanceFromGround(self):
        # x z y, le y nous indique la proximité du sol et le centre du robot
        cubePos, cubeOrn = p.getBasePositionAndOrientation(self.robotId)
        return cubePos[2]  # y, si < 0.15, on peut estimer qu'il est horizontal

    def getAngleWithGround(self):
        pass

    def computeFitness(self):
        pass
