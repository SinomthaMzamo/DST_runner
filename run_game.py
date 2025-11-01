import pgzrun
import random

from entities.player import Player
from game import Game

player_configuration = {
    'x': 150,
    'y': 300,
    'width': 40,
    'height': 80,
    }

score_counter = 0
game_state = "menu"   # ← NEW


# --- MENU BUTTONS ---
start_button = Rect(300, 180, 200, 60)
sound_button = Rect(300, 260, 200, 50)
music_button = Rect(300, 320, 200, 50)
exit_button = Rect(300, 380, 200, 50)

sound_on = True
music_on = True

game = Game(Player(player_configuration), sounds)

music.play('bg_music_welcome')
music.set_volume(0.5)

def on_mouse_down(pos):
    global game_state, sound_on, music_on

    if game_state == "menu":
        if start_button.collidepoint(pos):
            game_state = "playing"
        elif sound_button.collidepoint(pos):
            sound_on = not sound_on
        elif music_button.collidepoint(pos):
            music_on = not music_on
        elif exit_button.collidepoint(pos):
            exit()  

def on_key_down(key):
    global game_state
    if not game.game_started:
        if key == keys.SPACE:
            game.start_game()
            # update player state
            music.play('bg_music_playing')
            music.set_volume(0.5)
        return

    if game_state == 'playing':
        if game.control['game_over']:
            if key == keys.SPACE:
                game.reset()
            return

    
    
    # Jump - only allow if not sliding
    if key == keys.UP and not game.player.is_jumping and not game.player.is_sliding:
        game.player.jump()
        sounds.jump.play()

    elif game_state == 'menu' and key == keys.RETURN:
        game_state = 'playing'

def update():
        global score_counter 

        game.player.update_animation()

        if not game.game_started or game.control['game_over']:
            return
        
        if game_state != 'playing':
            return

        if game.control['game_over']:
            return
        
        # Increase the counter each frame
        score_counter += 1
        score_delay = 10  # how many frames to wait before adding 1 to the score

        # Update the score only every `score_delay` frames
        if score_counter >= score_delay:
            game.control['score'] += 1
            score_counter = 0  # reset counter
        
        # Increase game speed gradually
        if game.control['score'] % 500 == 0:
            game.control['game_speed'] += 0.2

        # Check if DOWN key is held for sliding
        if keyboard.down and not game.player.is_jumping:
            game.player.set_is_sliding(True) 
            game.player.update_state('is_running')
            sounds.slide.play()
        else:
            game.player.set_is_sliding(False) 

        # Player physics
        if not game.player.is_sliding:
            game.player.accelerate(game.control['player_gravity'])

            # Ground collision
            if game.player.y >= 300:
                game.player.land()
        else:
            # Keep player low while sliding
            game.player.slide()

        # Spawn obstacles
        game.obstacle_spawn_timer += 1
        if game.obstacle_spawn_timer >= game.obstacle_spawn_interval:
            if game.control['score'] % 7 == 0 and game.control['score'] > 30 and random.random() < 0.85:
                game.obstacles.append(game.create_obstacle(obstacle_type='platform'))
                # print("there's a platform!", game.control['score'], 'obs y:', game.obstacles[-1].y, 'actor y:', game.obstacles[-1].actor.y)
            else:
                game.obstacles.append(game.create_obstacle())
            game.obstacle_spawn_timer = 0
            # Randomize next spawn slightly
            game.obstacle_spawn_interval = random.randint(70, 110)

        game.update_obstacles()

def draw():
    screen.clear()

    if game_state == 'menu':
        draw_menu()
        return

    screen.fill((34, 32, 64))  # Night Sky blue
    # Draw ground grass
    screen.draw.filled_rect(Rect(0, game.control['ground_y'] + 40,Game.WIDTH, Game.HEIGHT - game.control['ground_y'] - 40), (44, 80, 44))
    # Draw ground soil
    screen.draw.filled_rect(Rect(0, game.control['ground_y'] + 80,Game.WIDTH, Game.HEIGHT), (60, 40, 20))

    game.player.actor.draw()

    if not game.game_started:
        screen.draw.text("Press SPACE to start", center=(Game.WIDTH // 2, Game.HEIGHT // 2),
                         color="white", fontsize=40)
        return

    # Draw obstacles
    for obs in game.obstacles:
        if obs.coin:
            obs.coin.draw()
        obs.actor.draw()
        # TODO: Debug outline for collisions
        screen.draw.rect(obs.actor._rect, (255, 0, 0))
        screen.draw.rect(game.player.actor._rect, (0, 255, 0))

    # Draw score
    screen.draw.text(f"Score: {int(game.control['score'])}", (10, 10), color='whitesmoke', fontsize=30)
    # Draw coins
    screen.draw.text(f"Coins: {int(game.collected_coins)}", (Game.WIDTH // 2, 10), color='whitesmoke', fontsize=30)
    # Draw instructions
    screen.draw.text("UP: Jump  DOWN: Slide", (10, 50), color='whitesmoke', fontsize=20)

    if game.control['game_over']:
        screen.draw.text("GAME OVER", center=(Game.WIDTH // 2, Game.HEIGHT // 2 - 30), 
                        color='firebrick', fontsize=60)
        screen.draw.text("Press SPACE to restart", center=(Game.WIDTH // 2, Game.HEIGHT // 2 + 30), 
                        color='thistle', fontsize=30)
        
def draw_menu():
    screen.fill((30, 30, 30))
    screen.draw.text("🚀 SPACE RUNNER 🚀", center=(Game.WIDTH // 2, 100), color="white", fontsize=60)

    # Buttons
    screen.draw.filled_rect(start_button, (100, 200, 100))
    screen.draw.text("Start Game", center=start_button.center, color="black", fontsize=40)

    screen.draw.filled_rect(sound_button, (180, 180, 180))
    screen.draw.text(f"Sound: {'On' if sound_on else 'Off'}", center=sound_button.center, color="black", fontsize=30)

    screen.draw.filled_rect(music_button, (180, 180, 180))
    screen.draw.text(f"Music: {'On' if music_on else 'Off'}", center=music_button.center, color="black", fontsize=30)

    screen.draw.filled_rect(exit_button, (200, 100, 100))
    screen.draw.text("Exit", center=exit_button.center, color="white", fontsize=40)

pgzrun.go()