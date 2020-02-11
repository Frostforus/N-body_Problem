from graphics import *
from math import sqrt, pi, cos, sin
import time


class System:
    __slots__ = ["size", "max_planets", "planets", "gamma", "scale"]

    def __init__(self, size=500, max_planets=3, gamma=20, scale=1, symmetry=0):
        self.size = size
        self.max_planets = max_planets
        self.planets = []
        self.gamma = gamma
        self.scale = scale
        if not symmetry:
            self.add_planets(Planet(name="Sôl", mass=2500, color="yellow", fix=True),
                             Planet(name="Mercury", mass=1, velocity=[0, 25], position=[50, 0], color="grey"),
                             Planet(name="Venus", mass=1.85, velocity=[0, -15], position=[-100, 0]),
                             Planet(name="Terra", mass=2, velocity=[-5, 0], position=[0, 290], color="blue"),
                             Planet(name="Mars", mass=1.2, velocity=[15, 0], position=[0, -290], color="orange"),
                             Planet(name="Iuppiter", mass=200, velocity=[5, -5], position=[-300, -290], color="brown"),
                             Planet(name="Saturnus", mass=150, velocity=[-5, 5], position=[300, 290], color="Yellow",
                                    ring=25),
                             Comet("Halley's Comet", mass=2, velocity=[5, 5], position=[300, -290], color="light blue")
                             )
        else:
            self.add_planets(Planet(name="Sol", mass=1000, color="yellow", fix=True))
            for i in range(max_planets - 1):
                self.add_planets(
                    Planet(name=i, mass=1, velocity=self.point_velocity(15, i, max_planets - 1),
                           position=self.point(symmetry, i, max_planets - 1), color="white"))

    def point(self, r, currentpoint, totalpoints):
        theta = pi * 2 / totalpoints
        angle = theta * currentpoint
        position = [r * cos(angle), r * sin(angle)]
        return position

    def point_velocity(self, speed, currentpoint, totalpoints):
        theta = pi * 2 / totalpoints
        angle = theta * currentpoint
        position = [speed * cos(angle + pi / 2), speed * sin(angle + pi / 2)]
        return position

    def add_planets(self, *args):
        for planet in args:
            if len(self.planets) < self.max_planets:
                self.planets.append(planet)
            else:
                print("Too many Planets")

    # TODO: Collide function; if the two planets are closer than then sum of their radius then the smaller ones mass
    #  is added to the larger ones, while it is destroyed
    def collide(self, planet_1, planet_2):
        if sqrt((planet_1.position[0] - planet_2.position[0]) ** 2 + (
                planet_1.position[1] - planet_2.position[1]) ** 2) < planet_1.get_radius() + planet_2.get_radius():
            print(planet_1.name, " and ", planet_2.name, "collided.")
            if planet_1.mass < planet_2.mass:
                self.planets.remove(planet_1)
                planet_2.mass += planet_1.mass
                print(planet_2.name, "'s new mass: ", planet_2.mass, " kg")
            else:
                self.planets.remove(planet_2)
                planet_1.mass += planet_2.mass
                print(planet_1.name, "'s new mass: ", planet_1.mass, " kg")

    def update(self, simulation_speed=1.0):
        # runs through all the planets
        for i in self.planets:
            # move based on last velocity

            i.update(position=i.velocity)
            # temp array
            calc_arr = []
            for p in self.planets:
                calc_arr.append(p)
            calc_arr.remove(i)
            # Physics calculation

            forces_array = []
            for p in calc_arr:
                r = sqrt((i.position[0] - p.position[0]) ** 2 + (i.position[1] - p.position[1]) ** 2)

                force_magnitude = self.gamma * (i.mass * p.mass) * -1 / (r ** 2)

                self.collide(i, p)

                force = [0, 0]
                force[0] = (i.position[0] - p.position[0]) * force_magnitude / r
                force[1] = (i.position[1] - p.position[1]) * force_magnitude / r
                forces_array.append(force)

            final_vector = [0, 0]
            for f in range(len(forces_array)):
                if f == 0:
                    final_vector[0] = forces_array[0][0] / (i.mass * simulation_speed)
                    final_vector[1] = forces_array[0][1] / (i.mass * simulation_speed)

                else:
                    final_vector[0] += forces_array[f][0] / (i.mass * simulation_speed)
                    final_vector[1] += forces_array[f][1] / (i.mass * simulation_speed)

            i.update(velocity=final_vector)

    def print(self, win, printstuff=False):

        for i in self.planets:
            i.draw(win)
            if printstuff:
                i.print()

    def start_simulation(self, max_time=100, simulation_speed=1, framerate=30):
        # Header initializes window
        simulation_speed = 1 / simulation_speed

        win = GraphWin("N-Body Problem", self.size, self.size, autoflush=False)
        win.setBackground("black")
        win.setCoords(-self.size / (2 * self.scale), -self.size / (2 * self.scale), self.size / (2 * self.scale),
                      self.size / (2 * self.scale))

        # Body
        start_time = time.time()
        current_time = time.time()

        while win.checkMouse() is None:
            #FIXME this should be drawspeed
            if simulation_speed < time.time() - current_time:

                current_time = time.time()
                # draw update to window
                win.delete("all")
                # TODO ezen belul legyen
                self.update(simulation_speed)
                self.print(win)
            # If max time is exceeded break out of loop
            elif max_time < time.time() - start_time:
                break
            else:
                continue
            # If time passed is greater than refresh rate, refresh
            # TODO lehet ezt az updaten belul kulon is kene kezelni
            update(framerate)

        # Trailer closes window
        win.close()
        print("Simulation successful")


class Planet:
    __slots__ = ["name", "mass", "velocity", "position", "trail", "color", "outline_color", "ring", "fix",
                 "add_to_trail"]

    def __init__(self, name, mass=1.0, velocity=None, position=None, color="white", outline_color="black", ring=0,
                 fix=False):
        self.name = name
        self.mass = mass
        self.velocity = [0, 0] if velocity is None else velocity
        self.position = [0, 0] if position is None else position
        self.color = color
        self.outline_color = outline_color
        self.ring = ring
        self.fix = fix
        self.trail = []
        self.add_to_trail = True

    def get_radius(self):
        return max(sqrt(self.mass), 2)

    # Adds given velocity or position to current
    def update(self, velocity=None, position=None):
        if self.fix:
            return
        if velocity is None:
            self.velocity = self.velocity
        else:

            self.velocity[0] = self.velocity[0] + velocity[0]
            self.velocity[1] = self.velocity[1] + velocity[1]

        if position is None:
            self.position = self.position
        else:
            # TODO: debug
            if len(self.trail) >= 15:
                self.trail.pop(0)
            if self.add_to_trail:
                self.trail.append([float(self.position[0]), float(self.position[1])])
                self.add_to_trail = True
            else:
                self.add_to_trail = True

            self.position[0] = self.position[0] + position[0]
            self.position[1] = self.position[1] + position[1]

    # TODO egyedi shapek kulon megrajzolása  végül egy draw ami meghívja az összeset, hogy a cometnek is legyen trailje
    def draw(self, win, draw_trail=True):
        # Draw trail
        if draw_trail:
            i = 1
            last_point = [0, 0]
            last_point[0] = self.position[0]
            last_point[1] = self.position[1]
            while i <= len(self.trail):
                line = Line(Point(last_point[0], last_point[1]), Point(self.trail[-i][0], self.trail[-i][1]))
                line.setWidth(1)
                line.setFill("white")
                line.draw(win)
                last_point[0] = self.trail[-i][0]
                last_point[1] = self.trail[-i][1]
                i += 1

        # If Planet has Ring draw it
        if self.ring:
            temp_ring = Circle(Point(self.position[0], self.position[1]), self.ring)
            temp_ring.setFill("black")
            temp_ring.setOutline("white")
            temp_ring.draw(win)

            temp_ring = Circle(Point(self.position[0], self.position[1]), self.ring - 3)
            temp_ring.setFill("dark gray")
            temp_ring.setOutline("white")
            temp_ring.draw(win)

        # Draw planet
        temp_circle = Circle(Point(self.position[0], self.position[1]), self.get_radius())
        temp_circle.setOutline(self.outline_color)
        temp_circle.setFill(self.color)
        temp_circle.draw(win)

    def print(self):
        print("Name:\t\t", self.name)
        print("Mass:\t\t", self.mass)
        print("Velocity:\t", self.velocity)
        print("Position:\t", self.position, end="\n\n")


class Comet(Planet):
    def draw(self, win, size=0.6):
        line = Line(Point(self.position[0], self.position[1]),
                    Point((self.position[0] - self.velocity[0]) * (1 / size),
                          (self.position[1] - self.velocity[1]) * (1 / size)))
        line.setFill("white")
        line.setWidth(2)
        line.draw(win)

        temp_circle = Circle(Point(self.position[0], self.position[1]), self.get_radius())
        temp_circle.setOutline(self.outline_color)
        temp_circle.setFill(self.color)
        temp_circle.draw(win)
