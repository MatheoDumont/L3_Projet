import pybullet as p

from genetic import *

class Robot:

    def __init__(self, start_pos, start_orientation):
        self.start_pos = start_pos
        self.robotId = p.loadURDF(
            "balance.urdf", start_pos, start_orientation)
        self.left_join = 0
        self.right_join = 1

        self.means_distance_from_ground = 1
        self.genes = []
        self.model = None
        self.num_step = 0
        self.vitesse = 1
        self.alive = True
        self.tick_stand_up = 0

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
        # on fait la moyenne pour la run du robot de la
        # distance entre son centre et le sol
        self.num_step += 1
        
        if self.alive:
            self.tick_stand_up += 1
            self.means_distance_from_ground = (self.means_distance_from_ground +
                                           self.getDistanceFromGround()) / self.num_step
            self.predict_vitesse()
            self.moveRobot(self.vitesse, self.vitesse)

            if self.getDistanceFromGround() < 0.04:
                self.alive = False


    def predict_vitesse(self):
        predict_input = np.array([self.vitesse, self.getDistanceFromGround()]).reshape(1, 2)
        self.vitesse = min(100, self.model.predict_on_batch([predict_input]) * 100)

    def getAngularSpeed(self):
        linear, angular = p.getBaseVelocity(self.robotId)
        return angular

    def load_model(self):
        self.model = gen_NN(self.genes)

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

		"means_distance_from_ground" est calculé à nouveau à chaque step
		pour avoir la moyenne de la run
        
        50 % pour le nombre de tick resté debout
        25 % pour "means_distance_from_ground"
        25 % pour la distance parcourue depuis le départ de la run pour le robot
        """
        

        return (self.means_distance_from_ground * 0.25 + (self.tick_stand_up / 10) * 0.5 +
            abs(p.getBasePositionAndOrientation(self.robotId)[0][0]) * 0.25)

    def reset(self):
        self.alive = True
        self.vitesse = 1
        self.num_step = 0
        self.means_distance_from_ground = 1
        self.tick_stand_up = 0

