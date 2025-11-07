# ui/buttons.py
from pgzero.rect import Rect
from constants import WIDTH, HEIGHT

def create_menu_buttons(button_specs, start_x, start_y, button_width, gap_y):
    """
    Automatically creates Rects for a vertical menu layout.

    Args:
        button_specs (list[tuple]): List of tuples in the form
            (name, height, col_span)
            where col_span determines if the button should take a full row (1)
            or share a row with another (0.5)
        start_x (int): X-coordinate of the first button.
        start_y (int): Y-coordinate of the first button.
        button_width (int): Width of a full-width button.
        gap_y (int): Vertical spacing between rows.

    Returns:
        dict[str, Rect]: Dictionary mapping button names to pygame.Rects
    """
    buttons = {}
    current_y = start_y
    half_width = (button_width // 2) - 5  # For paired buttons
    pending_half = None  # To track if a half-width button is waiting for a partner

    for name, height, col_span in button_specs:
        if col_span == 1:  # Full-width button
            buttons[name] = Rect(start_x, current_y, button_width, height)
            current_y += height + gap_y
        elif col_span == 0.5:
            if pending_half is None:
                # First half of a pair (left)
                buttons[name] = Rect(start_x, current_y, half_width, height)
                pending_half = (name, height)
            else:
                # Second half of a pair (right)
                left_name, left_height = pending_half
                buttons[name] = Rect(start_x + half_width + 10, current_y, half_width, height)
                # Reset and move to next row
                pending_half = None
                current_y += max(left_height, height) + gap_y

    # If there was a dangling half button, move down
    if pending_half is not None:
        current_y += pending_half[1] + gap_y

    return buttons


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
menu_button = Rect(10, HEIGHT - 100, 100, 40)

pause_button = Rect(10, HEIGHT - 50, 100, 40) 