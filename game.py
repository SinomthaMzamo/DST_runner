import random
from mission_classes import Mission
from entities.enemies import Enemy
from entities.player import Player
from pygame import Rect
from constants import obstacle_configurations, CoinAllocation

class Game:

    def __init__(self, player:Player, audio_manager):
        self.obstacles:list[Enemy] = []
        self.obstacle_spawn_timer = 0
        self.obstacle_spawn_interval = 90
        self.game_over = False
        self.mission_success = False
        self.game_speed = 5
        self.player_gravity = 0.8
        self.player = player
        self.mode = "arcade"
        self.current_mission = None

        self.round_score = 0
        self.highscore = 0
        self.has_achieved_new_high_score = False
        self.round_collected_vault_balance = 0
        self.total_collected_vault_balance = 0

        self.game_started = False
        self.game_over_processed = False
        self.audio_manager = audio_manager

    def set_current_mission(self, mission:Mission):
        self.current_mission = mission

    def do_game_over(self):
        if not self.game_over_processed and self.new_highscore():
            self.total_collected_vault_balance += self.round_collected_vault_balance
            if self.new_highscore():
                self.update_highscore()
                self.has_achieved_new_high_score = True
        self.game_over_processed = True

    def do_mission_success(self):
        if self.current_mission and self.current_mission.check_completion(self.round_score, self.round_collected_vault_balance):
            self.mission_success = True
            self.current_mission.complete = True
            self.current_mission.is_available = False
            return True
        return False
        
    def update_highscore(self):
        self.highscore = self.round_score

    def new_highscore(self):
        return self.round_score > self.highscore

    def start_game(self):
        self.game_started = True
        self.player.is_idling = False
        self.player.is_running = True

    def create_obstacle(self, obstacle_type=''):
        obstacle_type = random.choice(['ground', 'floating', 'floating-low']) if obstacle_type != 'platform' else  'platform'
        obstacle_configuration = obstacle_configurations[obstacle_type]
        obstacle = Enemy(obstacle_configuration, obstacle_type)
        return obstacle
    
    def coin_allocation_odds(self):
        return self.round_score % CoinAllocation.SCORE_DIVISIBILITY == 0 \
            and self.round_score > CoinAllocation.SCORE_COIN_ALLOCATION_THRESHOLD \
            and random.random() < CoinAllocation.COIN_ALLOCATION_ODDS
    
    def spawn_obstacles(self):
        # Spawn obstacles
        self.obstacle_spawn_timer += 1
        if self.obstacle_spawn_timer >= self.obstacle_spawn_interval:
            if self.coin_allocation_odds():
                self.obstacles.append(self.create_obstacle(obstacle_type='platform'))
            else:
                self.obstacles.append(self.create_obstacle())
            self.obstacle_spawn_timer = 0
            self.obstacle_spawn_interval = random.randint(70, 110)

    def reset(self):
        self.obstacles = []
        self.round_score = 0
        self.round_collected_vault_balance = 0
        self.game_over = False
        self.player.reset_state()
        self.obstacle_spawn_timer = 0
        self.game_speed = 5
        self.game_started = False
        self.has_achieved_new_high_score = False
        self.game_over_processed = False

    def update_obstacles(self):
        thresholds = {
            'ground': 25,
            'floating-low': 30,
            'floating': 20,
            'platform': 15
        }

        for obs in self.obstacles[:]:
            obs.update_x_position(self.game_speed)
            obs.update_movement()
            obs.update_enemy_frames()

            if obs.x < -obs.width:
                self.obstacles.remove(obs)
                continue

            obs.actor.x = obs.x
            obs.actor.y = obs.y
            threshold = thresholds.get(obs.obstacle_type, 10)

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
                    self.game_over = True
                    self.audio_manager.play_sound('collide', override=True)
                    self.audio_manager.play_sound('lose')

            if obs.coin and not obs.coin.collected and player_rect.colliderect(obs.coin.actor._rect):
                value_collected = obs.coin.collect()
                if value_collected:
                    self.audio_manager.play_sound('collect')
                    self.round_collected_vault_balance += value_collected


    def dump_player(self):
        return self.player.__str__()