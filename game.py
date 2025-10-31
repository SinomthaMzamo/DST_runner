import random
from entities.enemies import Enemy
from entities.player import Player

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

    def create_obstacle(self):
        obstacle_type = random.choice(['ground', 'floating', 'floating-low'])
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

    def update(self):
        if self.control['game_over']:
            return
        
        # Update score
        self.control['score'] += 1
        
        # Increase game speed gradually
        if self.control['score'] % 500 == 0:
            self.control['game_speed'] += 0.2

        # Check if DOWN key is held for sliding
        if keyboard.down and not self.player.is_jumping:
            self.player.set_is_sliding(True) 
        else:
            self.player.set_is_sliding(False) 

        # Player physics
        if not self.player.is_sliding:
            self.player.accelerate(self.control['player_gravity'])

            # Ground collision
            if self.player.y >= 300:
                self.player.collide()
        else:
            # Keep player low while sliding
            self.player.slide()

        # Spawn obstacles
        self.obstacle_spawn_timer += 1
        if self.obstacle_spawn_timer >= self.obstacle_spawn_interval:
            self.obstacles.append(self.create_obstacle())
            self.obstacle_spawn_timer = 0
            # Randomize next spawn slightly
            self.obstacle_spawn_interval = random.randint(70, 110)

        self.update_obstacles()

    def update_obstacles(self):
        # Update obstacles
        for obs in self.obstacles[:]:
            obs.update_x_position(self.control['game_speed'])
            obs.update_enemy_frames()
            # Remove off-screen obstacles
            if obs.x < - obs.width:
                self.obstacles.remove(obs)
            
            # Collision detection
            player_height = self.player.height // 2 if self.player.is_sliding else self.player.height
            player_left = self.player.x - self.player.width // 2
            player_right = self.player.x + self.player.width // 2
            player_bottom = self.player.y + player_height // 2
            player_top = self.player.y - player_height // 2
            
            obs_left = obs.x
            obs_right = obs.x + obs.width
            obs_top = obs.y - obs.height // 2
            obs_bottom = obs.y + obs.height // 2
            
            # Check collision
            if (player_right > obs_left and player_left < obs_right and
                player_bottom > obs_top and player_top < obs_bottom):
                self.control['game_over'] = True
        
