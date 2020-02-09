from graphics import *
import time


class System:
    __slots__ = ["size", "max_planets", "planets"]

    def __init__(self, size=500, max_planets=2):
        self.size = size
        self.max_planets = max_planets
        self.planets = []

        for i in range(max_planets):
            self.add_planet(Planet(name=i, mass=50,velocity=[10 * i, 10],position=[i  * 50, i * 50]))

    def add_planet(self, planet):
        if len(self.planets) <= self.max_planets:
            self.planets.append(planet)
        else:
            print("Too many Planets")

    def update(self, time_step=1.0, gamma=5):
        # runs through all the planets

        index = 0
        for i in self.planets:
            # move based on last velocity
            print("velocity: ", i.velocity)
            i.update(position=i.velocity)
            temp = [1, 1]
            temp[0] = i.velocity[0] * time_step
            temp[1] = i.velocity[1] * time_step

            # temp array
            calc_arr = []
            for p in self.planets:
                calc_arr.append(p)
            calc_arr.pop(index)
            # Physics calculation

            forces_array = []
            for p in calc_arr:
                r_2 = (i.position[0] - p.position[0]) ** 2 + (i.position[1] - p.position[1]) ** 2
                print("r_2 : ", r_2)
                force_magnitude = gamma * (i.mass * p.mass) * -1 / r_2
                force = [0, 0]
                force[0] = (i.position[0] - p.position[0]) * force_magnitude/ r_2
                force[1] = (i.position[1] - p.position[1]) * force_magnitude/ r_2
                forces_array.append(force)
            print(forces_array)
            final_vector = [0, 0]
            for f in range(len(forces_array)):
                if f == 0:
                    final_vector = forces_array[0]
                else:
                    final_vector[0] += forces_array[f][0]
                    final_vector[1] += forces_array[f][1]
            print(i.name,":FINAL VECTOR: ", final_vector)
            i.velocity[0] = final_vector[0]
            i.velocity[1] = final_vector[1]
            #i.update(velocity=final_vector)

            #for p in calc_arr:
                #p.print()
            index += 1

    def print(self, win):
        win.delete("all")
        for i in self.planets:
            temp_circle = Circle(Point(i.position[0], i.position[1]), i.mass / 15)
            temp_circle.setOutline("black")
            temp_circle.setFill(i.color)
            temp_circle.draw(win)
            #i.print()

    def start_simulation(self, max_time=100, time_step=1):
        # Header initializes window
        win = GraphWin("N-Body Problem", self.size, self.size)
        win.setBackground("black")
        win.setCoords(-self.size / 2, -self.size / 2, self.size / 2, self.size / 2)

        # Body
        start_time = time.time()
        current_time = time.time()

        while win.checkMouse() is None:
            # If time passed is greater than refresh rate, refresh
            if time_step < time.time() - current_time:
                current_time = time.time()
                # simulate physics here

                # draw update to window
                self.update(time_step=time_step)
                self.print(win)
            # If max time is exceeded break out of loop
            elif max_time < time.time() - start_time:
                break
            else:
                continue

        # Trailer closes window
        win.close()
        print("Simulation successful")


class Planet:
    __slots__ = ["name", "mass", "velocity", "position", "color"]

    def __init__(self, name, mass, velocity=None, position=None, color="white"):
        self.name = name
        self.mass = mass
        self.velocity = [0, 0] if velocity is None else velocity
        self.position = [0, 0] if position is None else position
        self.color = color

    # Adds given velocity or position to current
    def update(self, velocity=None, position=None):
        if velocity is None:
            self.velocity = self.velocity
        else:
            self.velocity[0] = self.velocity[0] + velocity[0]
            self.velocity[1] = self.velocity[1] + velocity[1]

        if position is None:
            self.position = self.position
        else:
            self.position[0] = self.position[0] + position[0]
            self.position[1] = self.position[1] + position[1]

    def print(self):
        print("Name:\t\t", self.name)
        print("Mass:\t\t", self.mass)
        print("Velocity:\t", self.velocity)
        print("Position:\t", self.position, end="\n\n")
