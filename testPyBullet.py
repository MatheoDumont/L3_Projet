import pybullet as p
import time
import pybullet_data

physicsClient = p.connect(p.GUI)#or p.DIRECT for non-graphical version
p.setAdditionalSearchPath(pybullet_data.getDataPath()) #optionally
p.setGravity(0,0,-100)
planeId = p.loadURDF("plane.urdf")
cubeStartPos = [0,0,1]
cubeStartOrientation = p.getQuaternionFromEuler([0,0,0])
boxId = p.loadURDF("balance.urdf",cubeStartPos, cubeStartOrientation)

print(p)
print("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")


for i in range (10000):

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
	#print(p.getBasePositionAndOrientation(boxId)[1])

  # pour savoir si le robot est tombé, on check une des coordonnées
	print(p.getBasePositionAndOrientation(boxId))
	p.stepSimulation()
	time.sleep(1./25.)
   	
cubePos, cubeOrn = p.getBasePositionAndOrientation(boxId)
print(cubePos,cubeOrn)
p.disconnect()
