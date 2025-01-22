import tkinter as tk
from tkinter import Frame, Label, Entry, Button, END

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import sim  # binded boost module


def set_text(entry, text):
    entry.delete(0, END)
    entry.insert(0, text)
    return


class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def clear(self):
        set_text(self.text_start_x, "0")
        set_text(self.text_start_y, "0")
        set_text(self.text_start_vx, "10")
        set_text(self.text_start_vy, "100")
        set_text(self.text_wind_vx, "-100")
        set_text(self.text_wind_vy, "0")
        set_text(self.text_gx, "0")
        set_text(self.text_gy, "-98.0")
        set_text(self.text_cross_section_area, "0.006")
        set_text(self.text_drag_coefficient, "0.45")
        set_text(self.text_mass, "0.05")
        set_text(self.text_fluid_density, "0.1")
        set_text(self.text_dt, "0.01")

    def restart(self):
        self.clear()
        self.ani.frame_seq = self.ani.new_frame_seq()

    def set_variables(self):
        self.position_start = sim.vector(
            float(self.text_start_x.get()), float(self.text_start_y.get())
        )

        self.velocity_start = sim.vector(
            float(self.text_start_vx.get()), float(self.text_start_vy.get())
        )
        self.velocity_wind = sim.vector(
            float(self.text_wind_vx.get()), float(self.text_wind_vy.get())
        )
        self.g = sim.vector(float(self.text_gx.get()), float(self.text_gy.get()))
        self.cross_section_area = float(self.text_cross_section_area.get())
        self.drag_coefficient = float(self.text_drag_coefficient.get())
        self.mass = float(self.text_mass.get())
        self.fluid_density = float(self.text_fluid_density.get())
        self.dt = float(self.text_dt.get())

    def run_sim(self):
        # read parameters
        self.set_variables()

        # define simulation
        bullet = sim.bullet(
            self.mass,
            self.position_start,
            self.velocity_start,
            self.cross_section_area * self.drag_coefficient,
        )
        cond = sim.external(self.fluid_density, self.velocity_wind, self.g)
        s = sim.simulation(bullet, cond, self.dt)

        # save oputput
        self.x, self.y = s.read_out()
        self.max_index = len(self.x)

    def animate(self, i):
        if i < self.max_index:
            xmin, xmax = self.ax.get_xlim()
            ymin, ymax = self.ax.get_ylim()

            # axes
            if self.x[i] >= xmax:
                self.ax.set_xlim(xmin, xmax + 100)
                self.ax.figure.canvas.draw()

            if self.x[i] <= xmin:
                self.ax.set_xlim(xmin - 100, xmax)
                self.ax.figure.canvas.draw()

            if self.y[i] >= ymax:
                self.ax.set_ylim(ymin, ymax + 100)
                self.ax.figure.canvas.draw()

            self.line.set_data(self.x[:i], self.y[:i])
        return (self.line,)

    def init_window(self):

        self.master.title("Simple GUI for testing C++ bindings")
        self.pack(fill="both", expand=1)

        # Create the controls, using grid
        self.label_start_x = Label(self, text="Start position X", width=20)
        self.label_start_x.grid(row=1, column=1)
        self.text_start_x = Entry(self, width=20)
        self.text_start_x.grid(row=1, column=2)

        self.label_start_y = Label(self, text="Start position Y", width=20)
        self.label_start_y.grid(row=2, column=1)
        self.text_start_y = Entry(self, width=20)
        self.text_start_y.grid(row=2, column=2)

        self.label_start_vx = Label(self, text="Start velocity X", width=20)
        self.label_start_vx.grid(row=3, column=1)
        self.text_start_vx = Entry(self, width=20)
        self.text_start_vx.grid(row=3, column=2)

        self.label_start_vy = Label(self, text="Start velocity Y", width=20)
        self.label_start_vy.grid(row=4, column=1)
        self.text_start_vy = Entry(self, width=20)
        self.text_start_vy.grid(row=4, column=2)

        self.label_wind_vx = Label(self, text="Wind velocity X", width=20)
        self.label_wind_vx.grid(row=5, column=1)
        self.text_wind_vx = Entry(self, width=20)
        self.text_wind_vx.grid(row=5, column=2)

        self.label_wind_vy = Label(self, text="Wind velocity Y", width=20)
        self.label_wind_vy.grid(row=6, column=1)
        self.text_wind_vy = Entry(self, width=20)
        self.text_wind_vy.grid(row=6, column=2)

        self.label_gx = Label(self, text="Gravity X", width=20)
        self.label_gx.grid(row=7, column=1)
        self.text_gx = Entry(self, width=20)
        self.text_gx.grid(row=7, column=2)

        self.label_gy = Label(self, text="Gravity Y", width=20)
        self.label_gy.grid(row=8, column=1)
        self.text_gy = Entry(self, width=20)
        self.text_gy.grid(row=8, column=2)

        self.label_cross_section_area = Label(self, text="Cross Area", width=20)
        self.label_cross_section_area.grid(row=9, column=1)
        self.text_cross_section_area = Entry(self, width=20)
        self.text_cross_section_area.grid(row=9, column=2)

        self.label_drag_coefficient = Label(self, text="Drag Coefficient", width=20)
        self.label_drag_coefficient.grid(row=10, column=1)
        self.text_drag_coefficient = Entry(self, width=20)
        self.text_drag_coefficient.grid(row=10, column=2)

        self.label_mass = Label(self, text="Mass", width=20)
        self.label_mass.grid(row=11, column=1)
        self.text_mass = Entry(self, width=20)
        self.text_mass.grid(row=11, column=2)

        self.label_fluid_density = Label(self, text="Fluid Density", width=20)
        self.label_fluid_density.grid(row=12, column=1)
        self.text_fluid_density = Entry(self, width=20)
        self.text_fluid_density.grid(row=12, column=2)

        self.label_dt = Label(self, text="Time Step (dt)", width=20)
        self.label_dt.grid(row=13, column=1)
        self.text_dt = Entry(self, width=20)
        self.text_dt.grid(row=13, column=2)

        self.clear()
        self.run_sim()

        self.button_apply = Button(self, text="Apply", command=self.run_sim, width=12)
        self.button_apply.grid(row=0, column=1)

        self.button_clear = Button(self, text="Restart", command=self.restart, width=12)
        self.button_clear.grid(row=0, column=2)

        self.button_clear.bind(lambda e: self.clear)

        tk.Label(self, text="Simulation").grid(column=3, row=0)

        self.fig = plt.Figure()

        self.ax = self.fig.add_subplot(111)
        (self.line,) = self.ax.plot([0], [0])

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(column=3, row=1, rowspan=13)

        self.ani = animation.FuncAnimation(
            self.fig, self.animate, interval=1, blit=True, repeat=False
        )


root = tk.Tk()
root.geometry("1000x600")
app = Window(root)
tk.mainloop()
