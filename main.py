# pylint: disable=W0312, C0111

from env import Env

ENV = Env()

if __name__ == "__main__":
    while True:
        ENV.step()
    ENV.disconnect()
