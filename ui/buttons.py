# ui/buttons.py
from pgzero.rect import Rect
from constants import WIDTH, HEIGHT
from sandbox import create_menu_buttons

# === MENU LAYOUT CONSTANTS ===
BUTTON_X = 200
BUTTON_Y = 150
BUTTON_WIDTH = 400
STANDARD_BUTTON_HEIGHT = 50
START_BUTTON_HEIGHT = 60
VERTICAL_BUTTON_GAP = 10
# VERTICAL_OFFSET = BUTTON_Y + START_BUTTON_HEIGHT + VERTICAL_BUTTON_GAP

button_configs = [
    ("start_button", START_BUTTON_HEIGHT, 1),        
    ("missions_button", STANDARD_BUTTON_HEIGHT, 0.5),     
    ("endless_button", STANDARD_BUTTON_HEIGHT, 0.5),      
    ("sound_button", STANDARD_BUTTON_HEIGHT, 0.5),      
    ("music_button", STANDARD_BUTTON_HEIGHT, 0.5),      
    ("exit_button", STANDARD_BUTTON_HEIGHT, 1),     
]

buttons = create_menu_buttons(button_configs, BUTTON_X, BUTTON_Y, BUTTON_WIDTH, VERTICAL_BUTTON_GAP)


# === MENU BUTTONS ===
start_button = buttons["start_button"]
missions_button = buttons["missions_button"]
endless_button = buttons["endless_button"]
sound_button = buttons["sound_button"]
music_button = buttons["music_button"]
exit_button = buttons["exit_button"]


# === IN-GAME MENU BUTTON ===
menu_button = Rect(WIDTH - 120, 10, 100, 40)
