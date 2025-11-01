from enum import Enum
from entities.entity import Entity
from pgzero.actor import Actor

class CoinValues(Enum):
    GOLD = 8
    SILVER = 4
    BRONZE = 2


class Coin(Entity):
    def __init__(self, configuration, value:CoinValues, sounds):
        super().__init__(configuration)
        self.value = value

        self.actor = Actor("reward-coin1.png", (self.x, self.y))
        self.collected = False
        self.spin_frames = [
            "reward-coin1.png", "reward-coin2.png", "reward-coin3.png",
            "reward-coin4.png", "reward-coin5.png", "reward-coin6.png"
        ]
        self.current_frame = 0
        self.frame_delay = 5
        self.frame_counter = 0
        self.sounds = sounds

    def update(self):
        self.frame_counter += 1
        if self.frame_counter % self.frame_delay == 0:
            self.current_frame = (self.current_frame + 1) % len(self.spin_frames)
            self.actor.image = self.spin_frames[self.current_frame]

    def draw(self):
        if not self.collected:
            self.actor.draw()

    def collect(self):
        if not self.collected:
            self.collected = True
            self.sounds.collect.play()
            return self.value.value
        return 0
