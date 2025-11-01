from  entities.rewards import Coin, CoinValues
from entities.entity import Entity
from pgzero.actor import Actor
from random import random


class Enemy(Entity):
    def __init__(self, configuration, obstacle_type):
        super().__init__(configuration)
        self.obstacle_type = obstacle_type
        self.color = self.set_enemy_colour()

        self.coin = None
        if self.obstacle_type == "platform" and random() < 0.8:  # 60% chance
            coin_y = self.y - 50  # float above the platform
            # print(f"Creating coin at ({self.x}, {coin_y}) for platform at y={self.y}")
            self.coin = Coin({'x':self.x, 'y':coin_y, 'width':50, 'height':50}, CoinValues.GOLD)

        # Add sprite animations
        self.floating_frames = ['enemy-blackhole1.png', 'enemy-blackhole2.png', 'enemy-blackhole3.png', 'enemy-blackhole4.png', 'enemy-blackhole5.png']
        self.floating_low_frames = ['enemy-debris1.png', 'enemy-debris2.png', 'enemy-debris3.png', 'enemy-debris4.png', 'enemy-debris5.png', 'enemy-debris6.png', 'enemy-debris7.png']
        self.ground_frames = ['enemy-volcano1.png', 'enemy-volcano2.png']
        self.cloud_frames = ['enemy-cloud001.png', 'enemy-cloud002.png', 'enemy-cloud003.png', 'enemy-cloud004.png', 'enemy-cloud005.png', 'enemy-cloud006.png']
        frames = self.get_frames_for_type()
        self.actor = Actor(frames[0], (self.x, self.y))
        self.current_frame = 0
        self.frame_delay = 6
        self.frame_counter = 0

        # For floating movement
        self.initial_y = self.y
        self.direction = 1  # 1 = up, -1 = down
        self.move_range = 20  # how far up/down to move
        self.move_speed = 1.5  # how fast to move

    def set_enemy_colour(self):
        if self.obstacle_type == 'ground':
            return (200, 50, 50)
        if self.obstacle_type == 'floating-low':
            return (10, 20, 200)
        if self.obstacle_type == 'floating':
            return (50, 50, 200)
        if self.obstacle_type == 'platform':
            return (255, 255, 255)
        
    def get_frames_for_type(self):
        if self.obstacle_type == 'floating':
            return self.floating_frames
        elif self.obstacle_type == 'floating-low':
            return self.floating_low_frames
        elif self.obstacle_type == 'platform':
            return self.cloud_frames
        else:
            return self.ground_frames
        
    def update_enemy_frames(self):
        if self.coin:
            self.coin.update()

        self.frame_counter += 1
        if self.frame_counter % self.frame_delay == 0:
            frames = self.get_frames_for_type()
            self.current_frame = (self.current_frame + 1) % len(frames)
            self.actor.image = frames[self.current_frame]

    def update_x_position(self, value):
        super().update_x_position(value) 
        self.actor.x = self.x  

        # Move coin with platform
        if self.coin:
            self.coin.x -= value  # move left with the platform
            self.coin.actor.x = self.coin.x

    def update_movement(self):
    # Horizontal movement is already handled elsewhere.
    
        # Floating-low oscillation
        if self.obstacle_type == "floating-low":
            self.y += self.direction * self.move_speed
            if abs(self.y - self.initial_y) > self.move_range:
                self.direction *= -1  # reverse direction
