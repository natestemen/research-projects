import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from .QuadTree import QuadTree
from .Body import Body

theta = 0.5
G = 1
epsilon = 0.01

def evolve(bodies, tmax, dt, xmax = 5, ymax = 5):
    time = 0
    while time <= tmax:
        T = QuadTree(ymax, xmax)
        for b in bodies:
            b.force = np.array([0.0,0.0])
            T.insert(b)
        T._time_step(dt)
        time += dt
    return [b.pos for b in bodies]
