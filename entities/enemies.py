from entities.entity import Entity

class Enemy(Entity):
    def __init__(self, configuration, type):
        super().__init__(configuration)
        self.type = type
        self.color = self.set_enemy_colour()

    def set_enemy_colour(self):
        if self.type == 'ground':
            return (200, 50, 50)
        if self.type == 'floating-low':
            return (10, 20, 200)
        if self.type == 'floating':
            return (50, 50, 200)

