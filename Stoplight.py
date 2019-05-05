import time
import threading
import queue
import numpy as np
from Cars import Car


class Stoplight:

    def __init__(self):
        self.right_turn_lanes = 0
        self.left_turn_lanes = 0
        self.straight_lanes = 2
        self.num_cars = 10
        self.cars_per_sec = 2
        self.left = 20
        self.right = 20
        self.time_green = 10
        self.light_transition_time = 1

        self.all_released = False
        self.cars_loading = True

        self.StopLightQueue = queue.Queue()
        self.Straight = queue.Queue()
        self.Left = queue.Queue()
        self.Right = queue.Queue()

        self.car_times = []

        # Amount of extra time it takes for a car to get going per car in front of it
        self.acceleration_delay_factor = 1

    def release_cars(self):

        i = 0
        while i < self.num_cars:
            for j in range(0, self.cars_per_sec):
                i += 1

                self.StopLightQueue.put(Car(i, self.left, self.right))
                if i >= self.num_cars:
                    break
            # Wait 1 sec after each batch of cars
            time.sleep(1)
        self.all_released = True
        print("all released")

    def load_lanes(self):
        while True:
            print("test")

            approaching_car = self.StopLightQueue.get()
            if self.StopLightQueue.empty() is True:
                print("Queue Empty")
                if self.all_released is True:
                    self.cars_loading = False
                    print("cars done loading")
                    return
                time.sleep(0.1)
                continue
            if approaching_car.direction is 'left' and self.left_turn_lanes > 0:
                self.Left.put(approaching_car)
            elif approaching_car is 'right' and self.right_turn_lanes > 0:
                self.Right.put(approaching_car)
            else:
                self.Straight.put(approaching_car)


    def green_light(self):
        print("light is green")
        time_end = time.time() + self.time_green
        while time.time() < time_end:
            # Handle left and right turn lanes
            for j in range(0, self.right_turn_lanes):
                car = self.Right.get()
                self.car_times.append(car.death())
            for j in range(0, self.left_turn_lanes):
                car = self.Left.get()
                self.car_times.append(car.death())
            for j in range(0, self.straight_lanes):
                car = self.Straight.get()
                self.car_times.append(car.death())

            # Wait time for a car in each lane to get going
            time.sleep(self.acceleration_delay_factor)

    def simulation(self):
        car_release_thread = threading.Thread(target=self.release_cars)
        car_release_thread.start()

        load_lanes_thread = threading.Thread(target=self.load_lanes)
        load_lanes_thread.start()



        while self.cars_loading is True or self.Straight.empty() is False \
                or self.Left.empty() is False or self.Right.empty() is False:
            time.sleep(self.time_green)
            time.sleep(self.light_transition_time)
            self.green_light()
            time.sleep(self.light_transition_time)
        print("end simulation")

    def calculate_latency(self):
        total_time = 0
        for i in range(0, len(self.car_times)):
            total_time += self.car_times[i]
        average_time = total_time / len(self.car_times)
        print(average_time)


test = Stoplight()
test.simulation()
test.calculate_latency()


