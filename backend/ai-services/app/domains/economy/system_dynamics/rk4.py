import numpy as np

class RK4Integrator:
    """
    Runge-Kutta 4th Order (RK4) numerical ODE solver.
    Provides extremely high precision for critical continuous variables (e.g., inflation curves).
    """
    def __init__(self, step_size=0.1):
        self.dt = step_size

    def step(self, func, t, y):
        """
        Takes one time step.
        :param func: Function f(t, y) returning the derivative dy/dt.
        :param t: Current time.
        :param y: Current state vector (numpy array).
        :return: New state vector at t + dt.
        """
        k1 = func(t, y)
        k2 = func(t + 0.5 * self.dt, y + 0.5 * self.dt * k1)
        k3 = func(t + 0.5 * self.dt, y + 0.5 * self.dt * k2)
        k4 = func(t + self.dt, y + self.dt * k3)

        new_y = y + (self.dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
        return new_y
