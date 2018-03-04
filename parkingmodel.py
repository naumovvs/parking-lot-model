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

    def  __init__(self, apt, duration):
        self.apt = apt
        self.duration = duration


class VehiclesFlow:

    def __init__(self, sim_time=24, s_intrv=Stochastic(), s_dur=Stochastic()):
        self.sim_duration = sim_time
        self.vehicles = []
        t = s_intrv.value()
        while (t < sim_time):
            self.vehicles.append(Vehicle(t, s_dur.value()))
            t += s_intrv.value()


class Parking:

    def __init__(self, capacity=20, vflow=VehiclesFlow()):
        self.capacity = capacity
        self.demand = vflow
        # working variables
        self.served = []
        self.rejected = []
        self.parked = []

    @property
    def occupancy(self):
        return len(self.parked)

    def simulate(self, t_step=1):
        vehicles = [v for v in self.demand.vehicles]
        t = 0
        model_error = 0

        while t < self.demand.sim_duration and len(vehicles) > 0:
            t += t_step
            # check if to leave
            for parked_vehicle in self.parked:
                if (parked_vehicle.apt + parked_vehicle.duration) < t:
                    self.served.append(parked_vehicle)
                    self.parked.remove(parked_vehicle)
                    #print "Vehicle ({},{}) left at {}".format(parked_vehicle.apt,\
                    #    parked_vehicle.duration, t)
                    model_error += t - (parked_vehicle.apt + parked_vehicle.duration)
            # check if to park
            v = vehicles[0]
            if v.apt < t:
                if self.occupancy < self.capacity:
                    #print "Vehicle ({},{}) parked in at {}".format(v.apt,\
                    #    v.duration, t)
                    self.parked.append(v)
                else:
                    #print "Vehicle ({},{}) rejected at {}".format(v.apt,\
                    #    v.duration, t)
                    self.rejected.append(v)
                model_error += t - v.apt
                vehicles.remove(v)
        #print "ERROR =", model_error


f = open("res.txt", 'w')

capacities = range(10, 30 * 5 + 10, 30)
arrivals = range(30, 120 * 5 + 30, 120)
durations = range(600, 1800 * 5 + 600, 1800)


for c in capacities:
    for a in arrivals:
        for d in durations:
           ps = []
           for _ in range(100):
               vf = VehiclesFlow(24*60*60, Stochastic("expon", p_scl=a),
                                 Stochastic("norm", d, 0.2 * d))
               p = Parking(c, vf)
               p.simulate()
               #print len(p.served), len(p.parked), len(vf.vehicles)
               ps.append(1.0 * (len(p.served) + len(p.parked)) / len(vf.vehicles))
           print c, a, d, sum(ps) / len(ps)
           f.write("{}\t{}\t{}\t{}\n".format(c, a, d, sum(ps) / len(ps)))
f.close()

#vf = VehiclesFlow(24, Stochastic("expon", p_scl=0.1),\
#    Stochastic("norm", 3, 0.5))
#print "DEMAND:"
#for v in vf.vehicles:
#    print v.apt, v.duration
#print
#print "SIMULATIONS:"
#p = Parking(3, vf)
#p.simulate()
#print
#print "Demand size:", len(p.demand.vehicles)
#print "Served number:", len(p.served)
#print "Rejected number:", len(p.rejected)
#print "Parked number:", len(p.parked)
