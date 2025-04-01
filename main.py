import pygame
import sys
from simulation import *


def main():

    simulation = Simulation(1600, 900)
    #simulation = Simulation(1366, 768)
    simulation.run()

if __name__ == "__main__":
    main()
