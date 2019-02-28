import pybullet as p


class Robot:

    def __init__(self, start_pos, start_orientation):
        self.start_pos = start_pos
        self.robotId = p.loadURDF(
            "balance.urdf", start_pos, start_orientation)
        self.left_join = 0
        self.right_join = 1

        self.means_distance_from_ground = 1

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

    def step(self, num_step):
        # on fait la moyenne pour la run du robot de la
        # distance entre son centre et le sol
        self.means_distance_from_ground = (self.means_distance_from_ground +
                                           self.getDistanceFromGround()) / num_step

    def getDistanceFromGround(self):
        # x z y, le y nous indique la proximité du sol et le centre du robot
        cubePos, cubeOrn = p.getBasePositionAndOrientation(self.robotId)
        return cubePos[2]  # y, si < 0.15, on peut estimer qu'il est horizontal

    def getAngleWithGround(self):
        pass

    def computeFitness(self):
        """
        ON CALCULE LA FITNESS A LA FIN

        Pour la fitness, on regarde la distance parcourue 
        ainsi que s'il est couché sur le sol ou toujours debout.

        Plus on est proche de 1 donc de la position debout
        plus on gagne de point
        75 % pour la moyenne de distance par rapport au sol
        25 % pour la distance parcourue depuis le départ de la run pour le robot
        """
        return (self.means_distance_from_ground * 0.75 + self.start_pos[0] * 0.25)
        
