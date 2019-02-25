from env import Env

env = Env()

if __name__ == "__main__":
	while True:
		env.step()
	env.disconnect()

