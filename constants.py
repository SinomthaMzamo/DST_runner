WIDTH = 800
HEIGHT = 500

COIN_ALLOCATION_ODDS = 0.85
SCORE_COIN_ALLOCATION_THRESHOLD = 30
SCORE_DIVISIBILITY = 7

player_configuration = {
    'x': 150,
    'y': 300,
    'width': 40,
    'height': 80,
}

control = {
    'ground_y': 290,
    'game_speed': 5,
    'score': 0,
    'game_over': False,
    'player_gravity': 0.8,
}

obstacle_configurations = {
    'ground': {
        'x': WIDTH,
        'y': control['ground_y']+10,
        'width': 40,
        'height': 60,
    },
    'floating-low': {
        'x': WIDTH,
        'y': control['ground_y']-10,
        'width': 50,
        'height': 50,
    },
    'floating': {
        'x': WIDTH,
        'y': control['ground_y']-25,
        'width': 50,
        'height': 60,
    },
    'platform': {
        'x': WIDTH,
        'y': 260,
        'width': 50,
        'height': 60,
    }
}
