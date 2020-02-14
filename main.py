# stable till like 20 planets coz of tiny miscalculations
from System import System

solar = System(size=600, max_planets=21, gamma=0.5, scale=0.1, max_time=150, symmetry=0)

solar.start_simulation(simulation_speed=30)

# TODO GITHUB COMMIT READY
#TODO Grav equations
