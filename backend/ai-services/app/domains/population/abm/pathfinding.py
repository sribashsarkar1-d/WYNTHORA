import heapq

class Node:
    def __init__(self, x, y, cost, heuristic):
        self.x = x
        self.y = y
        self.cost = cost
        self.heuristic = heuristic
        self.total = cost + heuristic
        self.parent = None

    def __lt__(self, other):
        return self.total < other.total

class AStarPathfinder:
    def __init__(self, grid_width, grid_height, obstacles=None):
        self.width = grid_width
        self.height = grid_height
        self.obstacles = set(obstacles) if obstacles else set()

    def heuristic(self, a, b):
        # Manhattan distance
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(self, node):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        neighbors = []
        for dx, dy in directions:
            nx, ny = node.x + dx, node.y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height and (nx, ny) not in self.obstacles:
                neighbors.append((nx, ny))
        return neighbors

    def find_path(self, start, goal):
        if start in self.obstacles or goal in self.obstacles:
            return []

        open_set = []
        heapq.heappush(open_set, Node(start[0], start[1], 0, self.heuristic(start, goal)))
        
        closed_set = set()
        came_from = {}
        g_score = {start: 0}

        while open_set:
            current = heapq.heappop(open_set)
            curr_pos = (current.x, current.y)

            if curr_pos == goal:
                path = []
                while curr_pos in came_from:
                    path.append(curr_pos)
                    curr_pos = came_from[curr_pos]
                path.reverse()
                return path

            closed_set.add(curr_pos)

            for nx, ny in self.get_neighbors(current):
                neighbor_pos = (nx, ny)
                if neighbor_pos in closed_set:
                    continue
                
                tentative_g = g_score[curr_pos] + 1 # cost is 1 per step
                
                if neighbor_pos not in g_score or tentative_g < g_score[neighbor_pos]:
                    came_from[neighbor_pos] = curr_pos
                    g_score[neighbor_pos] = tentative_g
                    h = self.heuristic(neighbor_pos, goal)
                    heapq.heappush(open_set, Node(nx, ny, tentative_g, h))
                    
        return [] # No path found
