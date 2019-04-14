import pybullet as p

from genetic import *


class Robot:

    def __init__(self, start_pos, start_orientation, model=None):
        self.start_pos = start_pos
        self.robotId = p.loadURDF(
            "balance.urdf", start_pos, start_orientation)
        self.left_join = 0
        self.right_join = 1

        self.means_distance_from_ground = 1
        if model is not None:
            self.model = model
        else:
            self.model = gen_NN()
        self.num_step = 0
        self.speed_left = 1
        self.speed_right = 1
        self.alive = True
        self.tick_stand_up = 0
        self.mean_diff_vitesse = 0

        linear, angular = self.getLinearAndAngularSpeed()
        start_input = np.array(
            [linear[0], linear[1], angular[0], angular[1], self.speed_left,
                self.speed_right, self.getDistanceFromGround()]
        )
        start_input = start_input.reshape(1, start_input.shape[0])

        self.prec_input = [start_input, start_input]

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
            self.means_distance_from_ground = (self.means_distance_from_ground * (self.num_step-1) + self.getDistanceFromGround()) / self.num_step
            #self.means_distance_from_ground = (self.means_distance_from_ground +
            #                                   self.getDistanceFromGround()) / self.num_step
            diff_vitesse = abs(self.speed_right - self.speed_left)
            self.mean_diff_vitesse = (self.mean_diff_vitesse * (self.num_step-1) + diff_vitesse) / self.num_step
            self.predict_vitesse()
            self.moveRobot(self.speed_left, self.speed_right)

            if self.getDistanceFromGround() < 0.15:
                # le bot meure
                self.alive = False
                # on met la vitesse a 0
                self.moveRobot(0, 0)
                orientation = p.getQuaternionFromEuler([0.1, 0, 0])
                p.resetBasePositionAndOrientation(
                    self.robotId, [0, -1000, 0], orientation)

    def predict_vitesse(self):
        linear, angular = self.getLinearAndAngularSpeed()

        predict_input = np.array(
            [linear[0], linear[1], angular[0], angular[1], self.speed_left,
                self.speed_right, self.getDistanceFromGround()]
        )
        predict_input = predict_input.reshape(1, predict_input.shape[0])
        input = np.hstack((predict_input, self.prec_input[1], self.prec_input[0]))

        self.prec_input[0] = self.prec_input[1]

        self.prec_input[1] = predict_input

        #print(input.shape)

        pred_left, pred_right = self.model.predict_on_batch(input)[0]
        self.speed_left = min(100, pred_left * 100)
        self.speed_right = min(100, pred_right * 100)
        #print(self.speed_right)

    def getLinearAndAngularSpeed(self):
        linear, angular = p.getBaseVelocity(self.robotId)
        return linear, angular

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
        #print(self.means_distance_from_ground)
        return (self.tick_stand_up) * (1 - self.means_distance_from_ground)**2 - (self.mean_diff_vitesse / 10)

    def reset(self):
        self.alive = True
        self.speed_left = 1
        self.speed_right = 1
        self.num_step = 0
        self.means_distance_from_ground = 1
        self.tick_stand_up = 0
        self.mean_diff_vitesse = 1
