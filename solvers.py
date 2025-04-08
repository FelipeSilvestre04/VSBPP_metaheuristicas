import numpy as np
import pyomo.environ as pyo


class ExactSolver:
    def __init__(self, instance):
        self.instance = instance
        print("ExactSolver: Solving the model using an exact solver.")
        solver = pyo.SolverFactory("gurobi")

