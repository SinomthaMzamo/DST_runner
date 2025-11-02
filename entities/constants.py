
"""
Game configuration constants.
All magic numbers should be defined here with clear names and documentation.
"""

# ==== WINDOW & DISPLAY ====
class Display:
    """Screen dimensions and layout"""
    WIDTH = 800
    HEIGHT = 400
    GROUND_Y = 290  # Where the ground starts
    GROUND_COLOR_TOP = (44, 80, 44)     # Grass green
    GROUND_COLOR_BOTTOM = (60, 40, 20)  # Dirt brown
    SKY_COLOR = (34, 32, 64)            # Dark purple space


# ==== PLAYER PHYSICS ====
class PlayerPhysics:
    """How the player moves and feels"""
    SPAWN_X = 150
    GROUND_Y = 300          # Standing position
    SLIDING_Y = 320         # Crouched position (20px lower)
    CLOUD_Y = 200           # When standing on platform
    
    JUMP_VELOCITY = -15     # Initial upward speed (negative = up)
    GRAVITY = 0.8           # How fast player falls
    
    # Animation speeds (frames to wait before next sprite)
    ANIM_SPEED_RUNNING = 6
    ANIM_SPEED_SLIDING = 6
    ANIM_SPEED_JUMPING = 6
    ANIM_SPEED_IDLE = 12    # Slower idle animation


# ==== GAME DIFFICULTY ====
class Difficulty:
    """Controls how hard the game gets"""
    INITIAL_SPEED = 5
    SPEED_INCREASE_INTERVAL = 500   # Score points between speed increases
    SPEED_INCREMENT = 0.2           # How much faster per increase
    
    # Obstacle spawning
    OBSTACLE_SPAWN_INTERVAL_MIN = 70   # Frames (fastest spawning)
    OBSTACLE_SPAWN_INTERVAL_MAX = 110  # Frames (slowest spawning)
    
    # Platform spawning (collectible coins on clouds)
    PLATFORM_MIN_SCORE = 30         # Don't spawn platforms until this score
    PLATFORM_SPAWN_CHANCE = 0.85    # 85% chance when conditions met
    PLATFORM_SCORE_DIVISOR = 7      # Only spawn when score divisible by this


# ==== SCORING ====
class Scoring:
    """Points and rewards"""
    SCORE_UPDATE_INTERVAL = 10  # Frames between score increments
    
    # Coin values (defined in CoinValues enum, but documented here)
    COIN_VALUE_GOLD = 8
    COIN_VALUE_SILVER = 4
    COIN_VALUE_BRONZE = 2


# ==== OBSTACLES ====
class ObstacleConfig:
    """Enemy and obstacle settings"""
    SPAWN_X = 800  # Off-screen right (same as Display.WIDTH)
    
    # Obstacle positions
    GROUND_Y = 300          # Ground obstacles
    FLOATING_LOW_Y = 280    # Low flying obstacles
    FLOATING_HIGH_Y = 260   # High flying obstacles
    PLATFORM_Y = 260        # Climbable platforms
    
    # Obstacle sizes
    GROUND_WIDTH = 40
    GROUND_HEIGHT = 60
    FLOATING_WIDTH = 50
    FLOATING_HEIGHT = 50
    PLATFORM_WIDTH = 50
    PLATFORM_HEIGHT = 60
    
    # Floating movement (oscillation)
    FLOAT_MOVE_RANGE = 12   # Pixels to move up/down
    FLOAT_MOVE_SPEED = 0.5  # Speed of oscillation
    
    # Animation
    ANIM_SPEED = 6  # Frames per animation frame


# ==== REWARDS ====
class RewardConfig:
    """Coin and collectible settings"""
    SIZE = 50  # Width and height of coins
    
    COIN_SPAWN_CHANCE = 0.8     # 80% of platforms get a coin
    COIN_HOVER_OFFSET = -50     # Pixels above platform (negative = up)
    
    ANIM_SPEED = 5  # Coin spin animation speed


# ==== COLLISION DETECTION ====
class Collision:
    """Hit box adjustments for fairer gameplay"""
    # These shrink the collision boxes so players don't die from near-misses
    THRESHOLD_GROUND = 25       # Ground obstacles (volcanoes)
    THRESHOLD_FLOATING_LOW = 30 # Low flying obstacles (debris)
    THRESHOLD_FLOATING_HIGH = 15 # High flying obstacles (black holes)
    THRESHOLD_PLATFORM = 15     # Platforms (clouds)
    THRESHOLD_DEFAULT = 10      # Fallback


# ==== MENU UI ====
class MenuUI:
    """Menu button positions and styling"""
    # Button dimensions
    BUTTON_WIDTH = 200
    BUTTON_HEIGHT_LARGE = 60  # Start button
    BUTTON_HEIGHT_SMALL = 50  # Toggle buttons
    
    # X position (centered)
    BUTTON_X = 300  # Left edge (800 - 200) / 2 = 300 for centered button
    
    # Y positions
    TITLE_Y = 100
    START_BUTTON_Y = 180
    SOUND_BUTTON_Y = 260
    MUSIC_BUTTON_Y = 320
    EXIT_BUTTON_Y = 380
    
    # Spacing between buttons
    BUTTON_SPACING = 60  # Pixels between button tops
    
    # Colors
    COLOR_START = (100, 200, 100)   # Green
    COLOR_TOGGLE = (180, 180, 180)  # Gray
    COLOR_EXIT = (200, 100, 100)    # Red


# ==== AUDIO ====
class Audio:
    """Sound and music settings"""
    MUSIC_VOLUME = 0.5  # 0.0 to 1.0
    
    # Track names
    MUSIC_MENU = 'bg_music_welcome'
    MUSIC_PLAYING = 'bg_music_playing'
    
    # Sound effect names
    SOUND_JUMP = 'jump'
    SOUND_SLIDE = 'slide'
    SOUND_COLLIDE = 'collide'
    SOUND_LOSE = 'lose'
    SOUND_COLLECT = 'collect'