from mesa import Model
from mesa.datacollection import DataCollector
from mesa.discrete_space import OrthogonalMooreGrid
from mesa.examples.basic.schelling.agents import SchellingAgent


class Schelling(Model):

    def __init__(
        self,
        height: int = 20,
        width: int = 20,
        density: float = 0.8,
        minority_pc: float = 0.5,
        homophily: float = 0.4,
        radius: int = 1,
        seed = None,
    ) -> None:
        
        super().__init__(seed=seed)

        self.density = density
        self.minority_pc = minority_pc

        self.grid = OrthogonalMooreGrid((width, height), random=self.random, capacity=1)

        self.happy = 0

        self.datacollector = DataCollector(
            model_reporters={
                "happy": "happy",
                "pct_happy": lambda m: (m.happy / len(m.agents)) * 100
                if len(m.agents) > 0
                else 0,
                "population": lambda m: len(m.agents),
                "minority_pct": lambda m: (
                    sum(1 for agent in m.agents if agent.type == 1)
                    / len(m.agents)
                    * 100
                    if len(m.agents) > 0
                    else 0
                ),
            },
            agent_reporters={"agent_type": "type"},
        )

        for cell in self.grid.all_cells:
            if self.random.random() < self.density:
                agent_type = 1 if self.random.random() < minority_pc else 0
                SchellingAgent(
                    self, cell, agent_type, homophily=homophily, radius=radius
                )

        self.agents.do("assign_state")
        self.datacollector.collect(self)

    def step(self) -> None:
        self.happy = 0  
        self.agents.shuffle_do("step")  
        self.agents.do("assign_state")
        self.datacollector.collect(self)  
        self.running = self.happy < len(self.agents)  