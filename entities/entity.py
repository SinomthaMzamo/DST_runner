class Entity:
    def __init__(self, configuration:dict):
        self.x = configuration['x']
        self.y = configuration['y']
        self.height = configuration['height']
        self.width = configuration['width']

    def set_x_position(self, value):
        self.x = value

    def set_y_position(self, value):
        self.y = value

    def update_x_position(self, value):
        self.x -= value

