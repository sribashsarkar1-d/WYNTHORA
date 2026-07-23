import numpy as np

class CellularAutomata:
    """
    Handles spatial spread across a 2D grid (e.g., disease spread, cultural influence).
    Uses Moore neighborhood (8 directions).
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # State grid: 0.0 to 1.0 (e.g., infection probability)
        self.grid = np.zeros((width, height), dtype=np.float32)

    def set_state(self, x, y, value):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[x, y] = value

    def step(self, spread_rate=0.1, decay_rate=0.01):
        """
        Computes one tick of the automata.
        """
        new_grid = np.copy(self.grid)
        
        for x in range(self.width):
            for y in range(self.height):
                # Calculate neighborhood sum
                x_min, x_max = max(0, x-1), min(self.width, x+2)
                y_min, y_max = max(0, y-1), min(self.height, y+2)
                
                neighborhood = self.grid[x_min:x_max, y_min:y_max]
                neighbor_sum = np.sum(neighborhood) - self.grid[x, y]
                
                # Apply rules: spread from neighbors, then natural decay
                increase = neighbor_sum * spread_rate
                new_val = self.grid[x,y] + increase - decay_rate
                
                # Clamp between 0.0 and 1.0
                new_grid[x, y] = np.clip(new_val, 0.0, 1.0)
                
        self.grid = new_grid

    def get_state(self, x, y):
        return self.grid[x, y]
