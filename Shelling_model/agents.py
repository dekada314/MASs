from mesa.discrete_space import CellAgent


class SchellingAgent(CellAgent):

    def __init__(
        self, model, cell, agent_type: int, homophily: float = 0.4, radius: int = 1
    ) -> None:
    
        super().__init__(model)
        self.cell = cell
        self.type = agent_type
        self.homophily = homophily
        self.radius = radius
        self.happy = False

    def assign_state(self) -> None:
        neighbors = list(self.cell.neighborhood.agents)

        similar_neighbors = len([n for n in neighbors if n.type == self.type])

        if (valid_neighbors := len(neighbors)) > 0:
            similarity_fraction = similar_neighbors / valid_neighbors
        else:
            similarity_fraction = 0.0

        if similarity_fraction < self.homophily:
            self.happy = False
        else:
            self.happy = True
            self.model.happy += 1

    def step(self) -> None:
        if not self.happy:
            self.cell = self.model.grid.select_random_empty_cell()