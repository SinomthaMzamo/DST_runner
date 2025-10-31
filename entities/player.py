from .entity import Entity

class Player(Entity):
    ''' Class representing the player '''
    DEFAULT_Y_POSITION = 300
    SLIDING_Y_POSITION = 320

    def __init__(self, configuration):
        super().__init__(configuration)
        # Add player-specific attributes
        self.vertical_velocity = 0
        self.jump_speed = -15
        self.is_jumping = False
        self.is_sliding = False      

    def set_is_jumping(self, state):
        self.is_jumping = state

    def set_is_sliding(self, state):
        self.is_sliding = state

    def set_vertical_velocity(self, value):
        self.vertical_velocity = value

    def reset_state(self):
        self.set_y_position(Player.DEFAULT_Y_POSITION)
        self.vertical_velocity = 0
        self.is_jumping = False
        self.is_sliding = False 

    def accelerate(self, gravity):
        self.vertical_velocity += gravity
        final_velocity = self.vertical_velocity + self.y
        self.set_y_position(final_velocity)
    
    def collide(self):
        self.set_y_position(Player.DEFAULT_Y_POSITION)
        self.vertical_velocity = 0
        self.is_jumping = False

    def slide(self):
        self.set_y_position(Player.SLIDING_Y_POSITION) 
        self.set_vertical_velocity(0)

    def jump(self):
        self.vertical_velocity = self.jump_speed
        self.is_jumping = True
