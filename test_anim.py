#!/usr/bin/env python

import sim  # simulation
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# initial conditions
position_start = sim.vector(0, 0)  # initial position (need to be >0)
velocity_start = sim.vector(10, 100)  # initial velocity
velocity_wind = sim.vector(-100, 0)  # wind velocity
g = sim.vector(0, -98.0665)  # gravitation force
cross_section_area = 6 * 0.001  # cross section area
drag_coefficient = 0.45  # drag coefficient
mass = 0.05  # bullet mass
fluid_density = 0.1  # air density
dt = 0.01  # time step

# simulation
bullet = sim.bullet(
    mass, position_start, velocity_start, cross_section_area * drag_coefficient
)
cond = sim.external(fluid_density, velocity_wind, g)
s = sim.simulation(bullet, cond, dt)
xx, yy = s.read_out()

# plotting
fig, ax = plt.subplots()
(line,) = ax.plot([], [], lw=2)
ax.set_ylim(0, 100)
ax.set_xlim(-100, 100)
ax.grid()

xdata, ydata = [], []
t_max = len(xx)
t = -1


def run(argument):
    global t
    t = t + 1
    if t >= t_max:
        return (line,)

    x = xx[t]
    y = yy[t]
    xdata.append(x)
    ydata.append(y)
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()

    # axes
    if x >= xmax:
        ax.set_xlim(xmin, xmax + 100)
        ax.figure.canvas.draw()

    if x <= xmin:
        ax.set_xlim(xmin - 100, xmax)
        ax.figure.canvas.draw()

    if y >= ymax:
        ax.set_ylim(ymin, ymax + 100)
        ax.figure.canvas.draw()

    line.set_data(xdata, ydata)

    return (line,)


ani = animation.FuncAnimation(fig, run, blit=True, interval=1, repeat=True)
plt.show()
