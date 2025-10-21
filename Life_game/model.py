from mesa.discrete_space import OrthogonalMooreGrid
from mesa import Model
from agents import Agent


class Life_game(Model):
    def __init__(self, seed = None, width = 50, height = 50, initial_fraction_alive = 0.2):
        super().__init__(seed=seed)
        
        self.grid = OrthogonalMooreGrid((width, height), capacity=1, torus=True)
        
        for cell in self.grid.all_cells:
            Agent(
                self,
                cell,
                init_state=Agent.ALIVE 
                if self.random.random() < initial_fraction_alive
                else Agent.DEAD,
            )
            
        self.running = True
        
    def step(self):
        self.agents.do('determine_state')
        self.agents.do('initial_state')