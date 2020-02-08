from graphics import *


class System:
    __slots__ = ["size", "max_planets", "planets"]

    def __init__(self, size=500, max_planets=2):
        self.size = size
        self.max_planets = max_planets
        self.planets = []

        for i in range(max_planets):
            self.add_planet(Planet(name=i, mass=(i + 1) * 100, position=[i * i * 25, i * i * 25]))

    def add_planet(self, planet):
        if len(self.planets) <= self.max_planets:
            self.planets.append(planet)
        else:
            print("Too many Planets")

    def print(self, win):
        for i in self.planets:
            temp_circle = Circle(Point(i.position[0], i.position[1]), i.mass / 15)
            temp_circle.setOutline("black")
            temp_circle.setFill(i.color)
            temp_circle.draw(win)
            i.print()

    def start_simulation(self, time_step=1):
        # Header initializes window
        win = GraphWin("N-Body Problem", self.size, self.size)
        win.setBackground("black")
        win.setCoords(-self.size / 2, -self.size / 2, self.size / 2, self.size / 2)

        # Body
        for i in range(0, 1000, time_step):
            # simulate physics here

            # draw update to window
            self.print(win)

        # Trailer closes window
        win.getMouse()
        win.close()
        print("Simulation successful")


class Planet:
    __slots__ = ["name", "mass", "velocity", "position", "color"]

    def __init__(self, name, mass, velocity=None, position=None, color="white"):
        self.name = name
        self.mass = mass
        self.velocity = [0, 1] if velocity is None else velocity
        self.position = [0, 0] if position is None else position
        self.color = color

    def update(self, velocity=None, position=None):
        self.velocity = self.velocity if velocity is None else velocity
        self.position = self.position if position is None else position

    def print(self):
        print("Name:\t\t", self.name)
        print("Mass:\t\t", self.mass)
        print("Velocity:\t", self.velocity)
        print("Position:\t", self.position, end="\n\n")
