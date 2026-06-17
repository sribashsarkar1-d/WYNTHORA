import numpy as np

class FiniteDifferencePDE:
    """
    Solves 1D Diffusion Equation: du/dt = alpha * d^2u/dx^2
    Using Finite Difference Method (FDM) explicit scheme.
    Used for modeling how CO2 disperses across longitudes.
    """
    def __init__(self, nx=50, length=100.0, alpha=0.5, dt=0.1):
        self.nx = nx                # Number of spatial grid points
        self.dx = length / (nx - 1) # Spatial step size
        self.alpha = alpha          # Diffusion coefficient
        self.dt = dt                # Time step
        
        # Stability check for explicit scheme: dt <= dx^2 / (2 * alpha)
        max_dt = (self.dx**2) / (2.0 * self.alpha)
        if self.dt > max_dt:
            print(f"Warning: PDE time step {self.dt} too large for stability. Max allowed: {max_dt}. Capping dt.")
            self.dt = max_dt
            
        self.u = np.zeros(nx)       # Initial concentration (e.g. CO2)

    def set_initial_condition(self, index, value):
        if 0 <= index < self.nx:
            self.u[index] = value

    def step(self):
        """
        Advances the diffusion equation by one time step dt.
        """
        u_new = np.copy(self.u)
        # Apply explicit finite difference formula to internal points
        for i in range(1, self.nx - 1):
            d2u_dx2 = (self.u[i+1] - 2*self.u[i] + self.u[i-1]) / (self.dx**2)
            u_new[i] = self.u[i] + self.alpha * self.dt * d2u_dx2
            
        # Optional: Apply Dirichlet boundary conditions (ends remain constant) or Neumann (insulated).
        # We'll leave boundaries fixed for now (u[0]=0, u[-1]=0 unless set).
        self.u = u_new
        return self.u
