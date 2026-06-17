import numpy as np

class EulerIntegrator:
    """
    Standard Euler Method numerical ODE solver.
    Fast and lightweight, used for low-precision linear growth models (e.g., population baselines).
    """
    def __init__(self, step_size=0.1):
        self.dt = step_size

    def step(self, func, t, y):
        """
        Takes one time step using y_{n+1} = y_n + dt * f(t_n, y_n)
        :param func: Function f(t, y) returning dy/dt.
        :param t: Current time.
        :param y: Current state vector (numpy array).
        :return: New state vector.
        """
        dy = func(t, y)
        new_y = y + self.dt * dy
        return new_y
