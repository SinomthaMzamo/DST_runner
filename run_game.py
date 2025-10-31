import pgzrun
import random

from entities.player import Player
from game import Game

config = {
    'x': 150,
    'y': 300,
    'width': 40,
    'height': 80,
    }
player = Player(config)
game = Game(player)

def on_key_down(key):
        if game.control['game_over']:
            if key == keys.SPACE:
                game.reset()
            return
        
        # Jump - only allow if not sliding
        if key == keys.UP and not game.player.is_jumping and not game.player.is_sliding:
            game.player.jump()

def update():
        if game.control['game_over']:
            return
        
        # Update score
        game.control['score'] += 1
        
        # Increase game speed gradually
        if game.control['score'] % 500 == 0:
            game.control['game_speed'] += 0.2

        # Check if DOWN key is held for sliding
        if keyboard.down and not game.player.is_jumping:
            game.player.set_is_sliding(True) 
        else:
            game.player.set_is_sliding(False) 

        # Player physics
        if not game.player.is_sliding:
            game.player.accelerate(game.control['player_gravity'])

            # Ground collision
            if game.player.y >= 300:
                game.player.collide()
        else:
            # Keep player low while sliding
            game.player.slide()

        # Spawn obstacles
        game.obstacle_spawn_timer += 1
        if game.obstacle_spawn_timer >= game.obstacle_spawn_interval:
            game.obstacles.append(game.create_obstacle())
            game.obstacle_spawn_timer = 0
            # Randomize next spawn slightly
            game.obstacle_spawn_interval = random.randint(70, 110)

        game.update_obstacles()

def draw():
    screen.clear()
    screen.fill((135, 206, 235))  # Sky blue

    # Draw ground
    screen.draw.filled_rect(Rect(0, game.control['ground_y'] + 40,Game.WIDTH, Game.HEIGHT - game.control['ground_y'] - 40), (100, 200, 100))

    # Draw player
    player_h = player.height // 2 if player.is_sliding else player.height
    screen.draw.filled_rect(
        Rect(player.x - player.width // 2, player.y - player_h // 2, player.width, player_h),
        (255, 200, 0)
    )

    # Draw obstacles
    for obs in game.obstacles:
        screen.draw.filled_rect(
            Rect(obs.x, obs.y - obs.height// 2, obs.width, obs.height),
            obs.color
        )

    # Draw score
    screen.draw.text(f"Score: {int(game.control['score'])}", (10, 10), color='black', fontsize=30)
    
    # Draw instructions
    screen.draw.text("UP: Jump  DOWN: Slide", (10, 50), color='black', fontsize=20)

    if game.control['game_over']:
        screen.draw.text("GAME OVER", center=(Game.WIDTH // 2, Game.HEIGHT // 2 - 30), 
                        color='red', fontsize=60)
        screen.draw.text("Press SPACE to restart", center=(Game.WIDTH // 2, Game.HEIGHT // 2 + 30), 
                        color='black', fontsize=30)
        
pgzrun.go()