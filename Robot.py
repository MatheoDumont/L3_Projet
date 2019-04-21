import pybullet as p
import numpy as np

from genetic import *


class Robot:

    def __init__(self, start_pos, start_orientation, model=None):
        self.start_pos = start_pos
        self.robotId = p.loadURDF(
            "balance.urdf", start_pos, start_orientation)
        self.left_join = 0
        self.right_join = 1

        if model is not None:
            self.model = model
        else:
            self.model = gen_NN()
        self.num_step = 0
        self.speed_left = 1
        self.speed_right = 1
        self.alive = True
        self.tick_stand_up = 0
        self.means_distance_from_ground = 1
        self.mean_diff_vitesse = 1
        self.mean_diff_ori = 1

        list_ori = []
        star_ori = p.getEulerFromQuaternion(start_orientation)
        for i in range(0, 10):
            list_ori.append(star_ori)

        self.prec_ori = np.array(list_ori)

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

            # calcul de la moyenne de la diff entre les vitesses des roues / agit comme une penalite
            diff_vitesse = abs(self.speed_right - self.speed_left)
            self.mean_diff_vitesse = (self.mean_diff_vitesse * (self.num_step-1) + diff_vitesse) / self.num_step

            # calcul de la difference entre l'orientation actuelle du robot sur le plan horizonal et l'orientation du robot dans le passe
            _, ori = p.getBasePositionAndOrientation(self.robotId)
            ori = p.getEulerFromQuaternion(ori)
            diff_ori = self.angle(ori, self.prec_ori[0]) * 100

            self.mean_diff_ori = (self.mean_diff_ori * (self.num_step-1) + diff_ori**2) / self.num_step

            for i in range(0, len(self.prec_ori)-2):
                self.prec_ori[i] = self.prec_ori[i+1]
            self.prec_ori[len(self.prec_ori)-1] = ori

            # effectue la prediction de la vitesse des 2 roues
            self.predict_vitesse()
            self.moveRobot(self.speed_left, self.speed_right)

            # si le bot est trop penche on considere qu'il est mort et on le teleporte en dehors du plateau
            if self.getDistanceFromGround() < 0.15:
                self.alive = False

                # on met la vitesse a 0
                self.moveRobot(0, 0)
                orientation = p.getQuaternionFromEuler([0, 0, 0])

                # on le teleporte en dehors du plateau
                p.resetBasePositionAndOrientation(
                    self.robotId, [0, -1000, 0], orientation)

    def predict_vitesse(self):
        linear, angular = self.getLinearAndAngularSpeed()
        _, ori = p.getBasePositionAndOrientation(self.robotId)
        ori = p.getEulerFromQuaternion(ori)
        
        # inputs avec les datas actuelles du robot
        predict_input = np.array(
            [linear[0], linear[1], angular[0], angular[1], self.speed_left, self.getDistanceFromGround()]
            # [linear[0], linear[1], linear[2], angular[0], angular[1], angular[2], self.speed_left, self.speed_right, ori[0], ori[1], ori[2]]
        )
        predict_input = predict_input.reshape(1, predict_input.shape[0])

        prediction = self.model.predict_on_batch(predict_input)[0][0]
        self.speed_left = min(100, prediction * 100)
        self.speed_right = min(100, prediction * 100)

    def getLinearAndAngularSpeed(self):
        linear, angular = p.getBaseVelocity(self.robotId)
        return linear, angular

    def load_model(self):
        self.model = gen_NN(self.genes)

    def getDistanceFromGround(self):
        # x z y, le y nous indique la proximité du sol et le centre du robot
        pos, _ = p.getBasePositionAndOrientation(self.robotId)
        return pos[2]  # y, si < 0.15, on peut estimer qu'il est horizontal

    def angle(self, v1, v2):
        # retourne l'angle entre les 2 vecteurs
        return math.acos((v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]) / (math.sqrt(v1[0]**2 + v1[1]**2 + v1[2]**2) * math.sqrt(v2[0]**2 + v2[1]**2 + v2[2]**2)))

    def getAngleWithGround(self):
        pass

    def computeFitness(self):
        # mean_diff_vittesse agit comme une penalite, on peut ajuster son importance, elle n'est utile que dans le cas ou le robot controle les 2 roues
        # mean_diff_ori agit comme une penalite, on peut ajuster son importance, elle n'est utile que dans le cas ou le robot controle les 2 roues
        # la distance moyenne au sol est "inverse" pour recompenser les robots qui restent bien droit
        return self.tick_stand_up * (1 - self.means_distance_from_ground)  # - self.mean_diff_ori / 20  # - (self.mean_diff_vitesse / 10)

    def reset(self):
        self.alive = True
        self.speed_left = 1
        self.speed_right = 1
        self.num_step = 0
        self.means_distance_from_ground = 1
        self.mean_diff_vitesse = 1
        self.mean_diff_ori = 1
        self.tick_stand_up = 0
