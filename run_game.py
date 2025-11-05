import os

from mission_classes import Mission, MissionManager

os.environ['SDL_VIDEO_CENTERED'] = '1'

import pgzrun

from entities.player import Player
from game import Game
from ui.buttons import (start_button, sound_button, music_button, exit_button, menu_button, missions_button, endless_button)
from ui.colours import *
from constants import player_configuration, HEIGHT, WIDTH, GameSettings

# === Audio Manager ===
class AudioManager:
    def __init__(self, sounds, music):
        self.sounds = sounds
        self.music = music
        self.sound_enabled = True
        self.music_enabled = True
        
    def play_sound(self, sound_name, override=False):
        if self.sound_enabled:
            if override:
                for s in self.sounds.__dict__.values():
                    try:
                        s.stop()
                    except AttributeError:
                        pass
            getattr(self.sounds, sound_name).play()

    
    def play_music(self, track_name, volume=0.2):
        if self.music_enabled:
            self.music.play(track_name)
            self.music.set_volume(volume)
    
    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        
    def toggle_music(self):
        self.music_enabled = not self.music_enabled
        if not self.music_enabled:
            self.music.stop()
        else:
            # Resume music based on game state
            audio_manager.play_music('bg_music_welcome', 0.1)

score_counter = 0
game_state = "menu" 

audio_manager = AudioManager(sounds, music)
game = Game(Player(player_configuration), audio_manager)
num_missions = 5
mission_manager = MissionManager(5)

audio_manager.play_music('bg_music_welcome', 0.2)

def on_mouse_down(pos):
    global game_state

    if game_state == "menu":
        if start_button.collidepoint(pos):
            game_state = "playing"
            if game.mode == "arcade":
                game_state = "playing"
            else:
                game_state = "missions"
        elif missions_button.collidepoint(pos):
            game.mode = "missions"
            print(game.mode)
        elif endless_button.collidepoint(pos):
            game.mode = "arcade"
            print(game.mode)
        elif sound_button.collidepoint(pos):
            audio_manager.toggle_sound()
        elif music_button.collidepoint(pos):
            audio_manager.toggle_music()
        elif exit_button.collidepoint(pos):
            exit()
    
    elif game_state == "missions":
        print(mission_manager.mission_and_button_list)
        for mission, button in mission_manager.mission_and_button_list:
            print("Checking", button[1], "button area:", button[0], "Miss is active:", mission.is_available)
            if button[0].collidepoint(pos):
                if mission.is_available:
                    mission_manager.assign_mission_to_game(game, mission)
                    game_state = "playing"
                    game.start_game()
                    break
                print("Mission", mission.level, "state", mission.is_available)

        # Back to main menu
        if menu_button.collidepoint(pos):
            game_state = "menu"

    elif game_state == "playing":
        if menu_button.collidepoint(pos):
            game.reset()
            audio_manager.music.stop()
            audio_manager.play_music('bg_music_welcome', 0.1)
            game_state = "menu"

def on_key_down(key):
    global game_state
    if not game.game_started:
        if key == keys.SPACE:
            game.start_game()
            audio_manager.play_music('bg_music_playing', 0.1)
        return

    if game_state == 'playing':
        if game.game_over:
            if key == keys.SPACE:
                game.reset()
            return
    
    if key == keys.UP and not game.player.is_jumping and not game.player.is_sliding:
        game.player.jump()
        audio_manager.play_sound('jump')

    elif game_state == 'menu' and key == keys.RETURN:
        game_state = 'playing'

def set_difficulty(game: Game, interval, speed_increase_factor):
     if game.round_score % interval == 0:
            game.game_speed += speed_increase_factor

def record_score():
    global score_counter

    score_counter += 1
    score_delay = 10  

    # Update the score only every `score_delay` frames
    if score_counter >= score_delay:
        game.round_score += 1
        score_counter = 0  # reset counter

def update():
    global score_counter 

    game.player.update_animation()
    mission_manager.complete_mission(game)
    if not game.game_started:
        return
    if game_state != 'playing':
        return
    if game.game_over:
        game.do_game_over()
        game.player.idle()
        return
    if game.mission_success:
        game.do_game_over()
        game.player.idle()
        return
    
    set_difficulty(game, 500, 0.4)
    record_score()

    if keyboard.down and not game.player.is_jumping:
        game.player.set_is_sliding(True) 
        game.player.update_state('is_running')
        audio_manager.play_sound('slide')
    else:
        game.player.set_is_sliding(False) 

    if not game.player.is_sliding:
        game.player.accelerate(game.player_gravity)
        if game.player.y >= Player.DEFAULT_Y_POSITION:
            game.player.land()
    else:
        game.player.slide()

    # Spawn obstacles
    game.spawn_obstacles()
    game.update_obstacles()

def draw_gradient(colour):
    screen.fill(colour)
    for i in range(0, HEIGHT, 10):
        # Slightly increase blue and decrease brightness as we go down
        shade = (
            max(0, colour[0] - i // 20),          # keep red low
            max(0, colour[1] - i // 30),          # reduce green slowly
            min(255, colour[2] + i // 15)         # increase blue slightly
        )
        screen.draw.filled_rect(Rect(0, i, WIDTH, 10), shade)

def draw():
    screen.clear()

    if game_state == 'menu':
        draw_menu()
        return
    elif game_state == "missions":
        draw_missions_screen()
    elif game_state == "playing":
        draw_game()

def draw_game():
    draw_gradient(SKY_COLOUR)
    screen.draw.filled_rect(Rect(0, GameSettings.GROUND_Y + 40, WIDTH, HEIGHT - GameSettings.GROUND_Y - 40), GROUND_TOP)
    screen.draw.filled_rect(Rect(0, GameSettings.GROUND_Y + 80, WIDTH, HEIGHT), GROUND_BOTTOM)

    game.player.actor.draw()

    if not game.game_started:
        screen.draw.text("Press SPACE to start", center=(WIDTH // 2, HEIGHT // 2), color="white", fontsize=40)
        # Draw Menu Button
        screen.draw.filled_rect(menu_button, BLUE)
        screen.draw.text("Menu", center=menu_button.center, color="white", fontsize=30)
        return

    # Draw obstacles
    for obs in game.obstacles:
        if obs.coin:
            obs.coin.draw()
        obs.actor.draw()

    in_mission = game.current_mission

    screen.draw.text(f"Score: {int(game.round_score)}" , (10, 10), color='whitesmoke', fontsize=30)
    screen.draw.text(
    f"High Score: {int(game.highscore)}" if not in_mission else f"Target Score: {int(game.current_mission.min_score)}",
    (10, 30),
    color='whitesmoke',
    fontsize=30
    )

    screen.draw.text(f"Round Balance: {int(game.round_collected_vault_balance)}", (WIDTH // 2, 10), color='whitesmoke', fontsize=30)
    screen.draw.text(
    f"Vault Balance: {int(game.total_collected_vault_balance)}" if not in_mission else f"Target Balance: {int(game.current_mission.vault_balance_required)}",
    (WIDTH // 2, 30),
    color='whitesmoke',
    fontsize=30
    )
    screen.draw.text("UP: Jump  DOWN: Slide", (10, 50), color='whitesmoke', fontsize=20)
    screen.draw.filled_rect(menu_button, BLUE)
    screen.draw.text("Menu", center=menu_button.center, color="white", fontsize=30)


    if game.current_mission and game.mission_success:
        print("yho")
        screen.draw.text("MISSION COMPLETE", center=(WIDTH // 2, HEIGHT // 2 - 30), 
                        color='green', fontsize=60)
        if game.has_achieved_new_high_score:
            screen.draw.text(f"New High Score: {game.highscore}", center=(WIDTH // 2, HEIGHT // 2 - 80), color='orange', fontsize=70)
            screen.draw.text("Press SPACE to restart", center=(WIDTH // 2, HEIGHT // 2 + 30), 
                        color='thistle', fontsize=30)

    elif game.game_over:
        screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2 - 30), 
                        color='firebrick', fontsize=60)
        if game.has_achieved_new_high_score:
            screen.draw.text(f"New High Score: {game.highscore}", center=(WIDTH // 2, HEIGHT // 2 - 80), color='orange', fontsize=70)
            screen.draw.text("Press SPACE to restart", center=(WIDTH // 2, HEIGHT // 2 + 30), 
                        color='thistle', fontsize=30)
        else:
            screen.draw.text("Press SPACE to restart", center=(WIDTH // 2, HEIGHT // 2 + 30), 
                        color='thistle', fontsize=30)
        
def draw_menu():
    draw_gradient(MENU_BG_COLOUR)

    screen.draw.text("SPACE RUNNER", center=(WIDTH // 2, 100), color="white", fontsize=70)

    screen.draw.filled_rect(start_button, GREEN)
    screen.draw.text("Start Game", center=start_button.center, color="black", fontsize=40)

    screen.draw.filled_rect(endless_button, YELLOW_ACTIVE if game.mode == 'arcade' else YELLOW_INACTIVE)
    screen.draw.text(f"Arcade mode", center=endless_button.center, color="black", fontsize=30)

    screen.draw.filled_rect(missions_button, YELLOW_ACTIVE if game.mode == 'missions' else YELLOW_INACTIVE)
    screen.draw.text(f"Mission mode", center=missions_button.center, color="black", fontsize=30)

    screen.draw.filled_rect(sound_button, GRAY)
    screen.draw.text(f"Sound: {'On' if audio_manager.sound_enabled else 'Off'}", center=sound_button.center, color="black", fontsize=30)

    screen.draw.filled_rect(music_button, GRAY)
    screen.draw.text(f"Music: {'On' if audio_manager.music_enabled else 'Off'}", center=music_button.center, color="black", fontsize=30)

    screen.draw.filled_rect(exit_button, RED)
    screen.draw.text("Exit", center=exit_button.center, color="white", fontsize=40)

def draw_missions_screen():
    draw_gradient(MENU_BG_COLOUR)
    screen.draw.text("MISSIONS", center=(WIDTH // 2, 50), color="white", fontsize=70)
    
    # for rect, level in mission_manager.buttons:
    #     screen.draw.filled_rect(rect, BLUE)
    #     screen.draw.text(f"Mission {level}", center=rect.center, color="white", fontsize=30)
    for mission, button in mission_manager.mission_and_button_list:
        rect, level = button
        screen.draw.filled_rect(rect, BLUE if mission.is_available else GRAY)
        screen.draw.text(f"Mission {level}", center=rect.center, color="white", fontsize=30)
        if mission.complete:
            #draw a green rect in button top left corner
            completion_rect = Rect(rect.left + 5, rect.top + 5, 20, 20)  # small 20x20 rectangle
            screen.draw.filled_rect(completion_rect, GREEN)  # green
    
    # Back button
    screen.draw.filled_rect(menu_button, RED)
    screen.draw.text("Back", center=menu_button.center, color="white", fontsize=30)


pgzrun.go()