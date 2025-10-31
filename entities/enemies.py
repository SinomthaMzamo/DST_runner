from entities.entity import Entity
from pgzero.actor import Actor


class Enemy(Entity):
    def __init__(self, configuration, type):
        super().__init__(configuration)
        self.type = type
        self.color = self.set_enemy_colour()
        # Add sprite animations
        self.floating_frames = ['enemy-blackhole1.png', 'enemy-blackhole2.png', 'enemy-blackhole3.png', 'enemy-blackhole4.png', 'enemy-blackhole5.png']
        self.floating_low_frames = ['enemy-debris1.png', 'enemy-debris2.png', 'enemy-debris3.png', 'enemy-debris4.png', 'enemy-debris5.png', 'enemy-debris6.png', 'enemy-debris7.png']
        self.ground_frames = ['enemy-volcano1.png', 'enemy-volcano2.png']
        frames = self.get_frames_for_type()
        self.actor = Actor(frames[0], (self.x, self.y))
        self.current_frame = 0
        self.frame_delay = 6
        self.frame_counter = 0

    def set_enemy_colour(self):
        if self.type == 'ground':
            return (200, 50, 50)
        if self.type == 'floating-low':
            return (10, 20, 200)
        if self.type == 'floating':
            return (50, 50, 200)
        
    def get_frames_for_type(self):
        if self.type == 'floating':
            return self.floating_frames
        elif self.type == 'floating-low':
            return self.floating_low_frames
        else:
            return self.ground_frames
        
    def update_enemy_frames(self):
        self.frame_counter += 1
        if self.frame_counter % self.frame_delay == 0:
            frames = self.get_frames_for_type()
            self.current_frame = (self.current_frame + 1) % len(frames)
            self.actor.image = frames[self.current_frame]


    def update_x_position(self, value):
        super().update_x_position(value) 
        self.actor.x = self.x  

