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
        self.num_cars = 50
        self.cars_per_sec = 2
        self.left = 20
        self.right = 20
        self.time_green = 10
        self.light_transition_time = 1

        self.all_released = False
        self.cars_loading = True

        self.sim_time_start = None
        self.sim_time_end = None

        self.StopLightQueue = queue.Queue()
        self.Straight = queue.Queue()
        self.Left = queue.Queue()
        self.Right = queue.Queue()
        self.EventQueue = queue.Queue()

        self.car_times = []
        self.latency_data = []
        self.throughput_data = []

        # Amount of extra time it takes for a car to get going per car in front of it
        self.acceleration_delay_factor = 1

        self.time_scale_factor = 10

    def release_cars(self):

        i = 0
        while i < self.num_cars:
            for j in range(0, self.cars_per_sec):
                i += 1

                self.StopLightQueue.put(Car(i, self.left, self.right))
                if i >= self.num_cars:
                    break
            # Wait 1 sec after each batch of cars
            time.sleep(1/self.time_scale_factor)
        self.EventQueue.get()

    def load_lanes(self):
        while True:
            try:
                approaching_car = self.StopLightQueue.get(block=False)
            except queue.Empty:
                if self.EventQueue.empty() is True:
                    self.cars_loading = False
                    return
                continue
            if approaching_car.direction is 'left' and self.left_turn_lanes > 0:
                self.Left.put(approaching_car)
            elif approaching_car is 'right' and self.right_turn_lanes > 0:
                self.Right.put(approaching_car)
            else:
                self.Straight.put(approaching_car)

    def green_light(self):
        time_end = time.time() + (self.time_green/self.time_scale_factor)
        while time.time() < time_end:
            if self.EventQueue.empty() is True and self.Straight.empty() is True \
                    and self.Left.empty() is True and self.Right.empty() is True:
                return 'done'
            for j in range(0, self.right_turn_lanes):
                try:
                    car = self.Right.get(block=False)
                except queue.Empty:
                    break
                self.car_times.append(car.death())
            for j in range(0, self.left_turn_lanes):
                try:
                    car = self.Left.get(block=False)
                except queue.Empty:
                    break
                self.car_times.append(car.death())
            for j in range(0, self.straight_lanes):
                try:
                    car = self.Straight.get(block=False)
                except queue.Empty:
                    break
                self.car_times.append(car.death())

            # Wait time for a car in each lane to get going
            time.sleep(self.acceleration_delay_factor/self.time_scale_factor)

    def simulation(self):
        self.car_times = []
        self.EventQueue.put("all released")
        self.sim_time_start = time.time()

        car_release_thread = threading.Thread(target=self.release_cars)
        car_release_thread.start()

        load_lanes_thread = threading.Thread(target=self.load_lanes)
        load_lanes_thread.start()

        while self.EventQueue.empty() is False or self.Straight.empty() is False \
                or self.Left.empty() is False or self.Right.empty() is False:
            time.sleep(self.time_green/self.time_scale_factor)
            time.sleep(self.light_transition_time/self.time_scale_factor)
            if self.green_light() is 'done':
                break
            time.sleep(self.light_transition_time/self.time_scale_factor)

        self.sim_time_end = time.time()
        print("end simulation")

    def calculate_latency(self):
        total_time = 0
        for i in range(0, len(self.car_times)):
            total_time += self.car_times[i]
        average_time = total_time / len(self.car_times)
        self.latency_data.append(average_time * self.time_scale_factor)

    def calculate_throughput(self):
        sim_time = self.sim_time_end - self.sim_time_start
        seconds_per_car = sim_time / self.num_cars
        self.throughput_data.append((1/seconds_per_car)*2)

    def reconfigure_test(self, right_lanes, left_lanes, straight, num, cps, left, right, green, yellow):
        self.right_turn_lanes = right_lanes
        self.left_turn_lanes = left_lanes
        self.straight_lanes = straight
        self.num_cars = num
        self.cars_per_sec = cps
        self.left = left
        self.right = right
        self.time_green = green
        self.light_transition_time = yellow

    def run_all_sims(self):
        self.reconfigure_test(1, 1, 2, 200, 4, 20, 20, 10, 4)
        self.simulation()
        self.calculate_latency()
        self.calculate_throughput()

        self.reconfigure_test(1, 1, 2, 200, 4, 20, 20, 20, 4)
        self.simulation()
        self.calculate_latency()
        self.calculate_throughput()

        self.reconfigure_test(1, 1, 2, 200, 4, 20, 20, 30, 4)
        self.simulation()
        self.calculate_latency()
        self.calculate_throughput()

        self.reconfigure_test(1, 1, 2, 200, 4, 20, 20, 40, 4)
        self.simulation()
        self.calculate_latency()
        self.calculate_throughput()

        self.reconfigure_test(1, 1, 2, 200, 4, 20, 20, 50, 4)
        self.simulation()
        self.calculate_latency()
        self.calculate_throughput()

        self.reconfigure_test(1, 1, 2, 200, 4, 20, 20, 60, 4)
        self.simulation()
        self.calculate_latency()
        self.calculate_throughput()

        print(self.latency_data)
        print(self.throughput_data)


test = Stoplight()
test.run_all_sims()


