import time
import random


class Car:

    def __init__(self, number, per_left, per_right):
        self.born = time.time()
        self.dead = None
        self.number = number
        randnum = random.randint(1, 101)

        if randnum < per_left:
            self.direction = 'left'
        elif 100 - randnum < per_right:
            self.direction = 'right'
        else:
            self.direction = 'center'

    def find_lane(self):
        print("test")
        pass

    def death(self):
        self.dead = time.time()
        return self.dead - self.born

