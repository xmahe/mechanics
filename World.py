class World:
    def __init__(self):
        self.nodes = list()
        self.interactions = list()
        self.clock = pygame.time.Clock()
        self.t = 0

    def add_node(self, node):
        self.nodes.append(node)

    def add_interaction(self, interaction):
        self.interactions.append(interaction)
