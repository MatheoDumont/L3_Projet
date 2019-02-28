
import pybullet as p
import time
import pybullet_data

physicsClient = p.connect(p.GUI)  # or p.DIRECT for non-graphical version
p.setAdditionalSearchPath(pybullet_data.getDataPath())  # optionally
p.setGravity(0, 0, -100)
planeId = p.loadURDF("plane.urdf")
cubeStartPos = [0, 0, 1]
cubeStartOrientation = p.getQuaternionFromEuler([0, 0, 0])
boxId = p.loadURDF("balance.urdf", cubeStartPos, cubeStartOrientation)


for i in range(10000):

    p.setJointMotorControl2(
        bodyUniqueId=boxId,
        jointIndex=0,
        controlMode=p.VELOCITY_CONTROL,
        targetVelocity=-100
    )
    p.setJointMotorControl2(
        bodyUniqueId=boxId,
        jointIndex=1,
        controlMode=p.VELOCITY_CONTROL,
        targetVelocity=100
    )
    cubePos, cubeOrn = p.getBasePositionAndOrientation(boxId)
    # x z y, le y nous indique la proximité du sol et le centre du robot
    torpint = 'POS x={} | z={} | y={} || ANGLE x={} | z={} | y={} '.format(
        cubePos[0], cubePos[1], cubePos[2], cubeOrn[0], cubeOrn[1], cubeOrn[2])
    print(torpint)
    if cubePos[2] < 0.037:
        print("----------------DEAD---------------------")

    p.stepSimulation()

    time.sleep(1. / 25.)


p.disconnect()
