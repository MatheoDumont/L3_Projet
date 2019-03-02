import pybullet as p
import time
import pybullet_data


"""
Le lien pour avoir plusieurs client pybullet DIRECT en parallèle
https://github.com/bulletphysics/bullet3/issues/1925
L'exemple sur github
https://github.com/bulletphysics/bullet3/blob/master/examples/pybullet/gym/pybullet_utils/examples/multipleScenes.py
"""

p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

planeId = p.loadURDF("plane.urdf", useMaximalCoordinates=False)
cubeId = p.loadURDF("cube_collisionfilter.urdf", [0,0,3], useMaximalCoordinates=False)
cubeId2 = p.loadURDF("cube_collisionfilter.urdf", [0,0,5], useMaximalCoordinates=False)

collisionFilterGroup = 0
collisionFilterMask = 0
p.setCollisionFilterGroupMask(cubeId,-1,collisionFilterGroup,collisionFilterMask)
p.setCollisionFilterGroupMask(cubeId2,-1,1,1)

enableCollision = 1
p.setCollisionFilterPair(planeId, cubeId,-1,-1,enableCollision )

p.setRealTimeSimulation(1)
p.setGravity(0,0,-10)
while (p.isConnected()):
	time.sleep(1./240.)
p.setGravity(0,0,-10)