import math

def growth_requirement(level: int, base: float, rate: float = 1.18, log_weight: float = 0.5) -> float:
    """
    Calculates a gradually increasing requirement using a hybrid exponential-logarithmic growth model.

    This model starts faster than pure exponential growth and slows slightly over time to avoid overly steep difficulty spikes.

    Formula:
        R(n) = base * (rate ** n) + (log_weight * base * log2(n + 1))

    Args:
        level (int): The mission or progression level (e.g. 1, 2, 3...).
        base (float): The base value for the first level (starting score or coin requirement).
        rate (float): The exponential rate (default 1.18). Higher = faster growth.
        log_weight (float): How much the logarithmic component contributes. 
                            Higher = slightly steeper start, slower late growth.

    Returns:
        int: The scaled requirement for the given level rounded to the nearest 10.
    """
    raw_value =  base * (rate ** level) + (log_weight * base * math.log2(level + 1))
    return int(round(raw_value / 10) * 10)

def get_score_requirement(level):
    return growth_requirement(level, base=120, rate=2.18, log_weight=0.5)

def get_vault_balance_requirement(level):
    return growth_requirement(level, base=50, rate=1.38, log_weight=0.3)

# for i in range(10):
#     print(get_score_requirement(i))

# for i in range(10):
#     print(get_vault_balance_requirement(i))


from pygame import Rect

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
