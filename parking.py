import math
import random

class Stochastic:

    def __init__(self, p_law="rect", p_loc=0, p_scl=1, p_sh=0):
        # rect, expon, norm, ...
        self.law = p_law
        self.location = p_loc
        self.scale = p_scl
        self.shape = p_sh

    def rect(self):
        return self.location + self.scale * random.random()

    def expon(self):
        return -self.scale * math.log(random.random())

    def norm(self):
        return self.location + self.scale * \
                (sum([random.random() for _ in range(12)]) - 6)

    def value(self):
        if self.law == "expon":
            return self.expon()
        elif self.law == "norm":
            return self.norm()
        else:
            return self.rect()


class Vehicle:

    def __init__(self, in_time, duration):
        self.in_parking_time = in_time
        self.parking_duration = duration

    @property
    def out_parking_time(self):
        return self.in_parking_time + self.parking_duration


class VehiclesFlow:

    def __init__(self, duration=24, intrv=Stochastic(), pdur=Stochastic()):
        self.vehicles = []
        sum_intrv = 0
        while sum_intrv < duration:
            sum_intrv += intrv.value()
            self.vehicles.append(Vehicle(sum_intrv, pdur.value()))

    @property
    def vehicles_number(self):
        return len(self.vehicles)

    def print_out(self):
        for v in self.vehicles:
            print v.in_parking_time, v.parking_duration

class Parking:

    def __init__(self, vf=VehiclesFlow(), capacity=100):
        self.demand = vf
        self.capacity = capacity
        self.currently_parked = []
        self.serviced = []
        self.rejected = []

    @property
    def occupancy(self):
        return len(self.currently_parked)

    def simulate(self, tStep=1):
        t = 0
        vehicles = [v for v in self.demand.vehicles]

        while (len(vehicles) > 0 or self.occupancy > 0):
            t += tStep
            if (len(vehicles) > 0):
                v = vehicles[0]
                if (v.in_parking_time <= t):
                    if (self.occupancy < self.capacity):
                        self.currently_parked.append(v)
                        self.serviced.append(v)
                        print "({}:{}) parked in {}".format(v.in_parking_time, v.parking_duration, t)
                        vehicles.remove(v)
                    else:
                        self.rejected.append(v)
                        print "({}:{}) rejected {}".format(v.in_parking_time, v.parking_duration, t)
                        vehicles.remove(v)

            if (self.occupancy > 0):
                leave = []
                for pv in self.currently_parked:
                    if (pv.out_parking_time <= t):
                        leave.append(pv)
                for lv in leave:
                    self.currently_parked.remove(lv)
                    print "({}:{}) parked out {}".format(lv.in_parking_time, lv.parking_duration, t)


p = Parking(VehiclesFlow(24, Stochastic(), Stochastic("norm", 10, 0.5)), 20)
print len(p.demand.vehicles)
p.simulate()
print len(p.serviced), len(p.rejected)
