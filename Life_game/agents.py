from mesa.discrete_space import FixedAgent


class Agent(FixedAgent):
    
    ALIVE = 1
    DEAD = 0
        
    @property
    def is_alive(self):
        return self.state == self.ALIVE
    
    @property
    def neighbors(self):
        return self.cell.neighborhood.agents
    
    def __init__(self, model, cell, init_state = 0):
        super().__init__(model)

        self.cell = cell
        
        self.state = init_state
        self.next_state = None
        
    def determine_state(self):
        live_neighbors = sum(neighbor.is_alive for neighbor in self.neighbors)
        self.next_state = self.state
        
        if self.is_alive:
            if live_neighbors < 2 or live_neighbors > 3:
                self.next_state = self.DEAD
        else:
            if live_neighbors == 3:
                self.next_state = self.ALIVE
        
    def initial_state(self):
        self.state = self.next_state