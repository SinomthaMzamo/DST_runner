import random
from entities.enemies import Enemy
from entities.player import Player
from pygame import Rect

class Game:
    WIDTH = 800
    HEIGHT = 400

    def __init__(self, player:Player):
        self.obstacles:list[Enemy] = []
        self.obstacle_spawn_timer = 0
        self.obstacle_spawn_interval = 90
        self.control = {
            'ground_y': 290,
            'game_speed': 5,
            'score': 0,
            'game_over': False,
            'player_gravity': 0.8,
        }
        self.player = player

    def create_obstacle(self, obstacle_type=''):
        obstacle_type = random.choice(['ground', 'floating', 'floating-low']) if obstacle_type != 'platform' else  'platform'
        obstacle_configurations = {
            'ground': {
                'x': Game.WIDTH,
                'y': self.control['ground_y']+10,
                'width': 40,
                'height': 60,
            },
            'floating-low': {
                'x': Game.WIDTH,
                'y': 280,
                'width': 50,
                'height': 50,
            },
            'floating': {
                'x': Game.WIDTH,
                'y': 260,
                'width': 50,
                'height': 60,
            },
            'platform': {
                'x': Game.WIDTH,
                'y': 260,
                'width': 50,
                'height': 60,
            }
        }

        obstacle_configuration = obstacle_configurations[obstacle_type]
        obstacle = Enemy(obstacle_configuration, obstacle_type)
        return obstacle
    
    def reset(self):
        self.obstacles = []
        self.control['score'] = 0
        self.control['game_over'] = False
        self.player.reset_state()
        self.obstacle_spawn_timer = 0
        self.control['game_speed'] = 5

    def update_obstacles(self):
        # COLLISION_THRESHOLD = 20  # ← you can tweak this (5–15 is typical)

        thresholds = {
            'ground': 25,
            'floating-low': 30,
            'floating': 15,
            'platform': 15
        }

        for obs in self.obstacles[:]:
            obs.update_x_position(self.control['game_speed'])
            obs.update_enemy_frames()

            # Remove off-screen obstacles
            if obs.x < -obs.width:
                self.obstacles.remove(obs)
                continue

            # Update actor position
            obs.actor.x = obs.x
            obs.actor.y = obs.y

            threshold = thresholds.get(obs.obstacle_type, 10)

            # Get shrunk rectangles
            player_rect = Rect(
                self.player.actor.x - self.player.actor.width / 2,
                self.player.actor.y - self.player.actor.height / 2,
                self.player.actor.width,
                self.player.actor.height
            ).inflate(-threshold, -threshold)

            obs_rect = Rect(
                obs.actor.x - obs.actor.width / 2,
                obs.actor.y - obs.actor.height / 2,
                obs.actor.width,
                obs.actor.height
            ).inflate(-threshold, -threshold)


            # ✅ Collision check with threshold
            if player_rect.colliderect(obs_rect):
                if obs.obstacle_type == 'platform':
                    self.player.land(Player.CLOUD_Y_POSITION)
                else:
                    self.control['game_over'] = True

            if obs.coin and player_rect.colliderect(obs.coin.actor._rect):
                obs.coin.collect()

        
