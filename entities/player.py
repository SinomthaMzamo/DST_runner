from enum import Enum
from .entity import Entity
from pgzero.actor import Actor

class PlayerState(Enum):
    RUNNING = 'is_running',
    SLIDING = 'is_sliding',
    JUMPING = 'is_jumping',
    IDLE = 'is_idle'    


class Player(Entity):
    ''' Class representing the player '''
    DEFAULT_Y_POSITION = 300
    SLIDING_Y_POSITION = 320
    CLOUD_Y_POSITION = 200

    def __init__(self, configuration):
        super().__init__(configuration)

        # Add player-specific attributes
        self.vertical_velocity = 0
        self.jump_speed = -15
        self.is_jumping = False
        self.is_sliding = False
        self.is_running = False
        self.is_idleing = True    

        # Add sprite animations
        self.running_frames = ['player-run024.png', 'player-run025.png', 'player-run026.png', 'player-run027.png', 'player-run028.png', 'player-run029.png', 'player-run030.png', 'player-run031.png']
        self.sliding_frames = ['player-slide10.png', 'player-slide11.png', 'player-slide12.png']
        self.jumping_frames = ['player-jump16.png', 'player-jump17.png', 'player-jump18.png', 'player-jump19.png', 'player-jump20.png']
        self.idle_frames = ['player-idle07.png', 'player-idle08.png']
        self.actor = Actor(self.idle_frames[0], (self.x, self.y))
        self.current_frame = 0
        self.frame_delay = 6
        self.frame_counter = 0

    def update_state(self, attribute):
        if attribute == 'is_running':
            self.is_running = not self.is_running
        if attribute == 'is_jumping':
            self.is_jumping = not self.is_jumping
        if attribute == 'is_sliding':
            self.is_sliding = not self.is_sliding

    def update_animation(self):
        self.frame_counter += 1
        if self.frame_counter % self.frame_delay == 0:
            if self.is_jumping:
                frames = self.jumping_frames
            elif self.is_sliding:
                frames = self.sliding_frames
            elif self.is_idleing:
                self.frame_delay = 12
                frames = self.idle_frames
            else:
                frames = self.running_frames
            
            self.current_frame = (self.current_frame + 1) % len(frames)
            self.actor.image = frames[self.current_frame]

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
        self.actor.y = final_velocity
    
    def land(self, position=None):
        """Called when the player lands on the ground."""
        if position is None:
            position = Player.DEFAULT_Y_POSITION

        self.set_y_position(position)
        self.actor.y = position
        self.vertical_velocity = 0
        self.is_jumping = False

    def slide(self):
        self.set_y_position(Player.SLIDING_Y_POSITION)
        self.actor.y = Player.SLIDING_Y_POSITION 
        self.set_vertical_velocity(0)

    def jump(self):
        self.vertical_velocity = self.jump_speed
        self.is_jumping = True
