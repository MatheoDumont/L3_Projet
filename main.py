# pylint: disable=W0312, C0111

from env import Env

ENV = Env()

if __name__ == "__main__":
    for i in range(1,100):
    	ENV.computeGeneration()
    ENV.disconnect()
