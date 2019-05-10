import time
import random


class Car:

    def __init__(self, number, per_left, per_right):
        self.born = time.time()  # Record time of car init
        self.dead = None
        self.number = number
        randnum = random.randint(1, 101)

        # Determine car direction based on a random number and specifications
        if randnum < per_left:
            self.direction = 'left'
        elif 100 - randnum < per_right:
            self.direction = 'right'
        else:
            self.direction = 'center'

    @staticmethod
    def find_lane():
        print("test")
        pass

    # Record time of car death and return total time car was alive
    def death(self):
        self.dead = time.time()
        return self.dead - self.born


