from pygame import Rect
from constants import WIDTH
from utils import get_score_requirement, get_vault_balance_requirement


class Mission:
    def __init__(self, level):
        self.level = level
        self.vault_balance_required = 0
        self.min_score = 0
        self.reward_multiplier = 0
        self.complete = False
        self.is_available = False
        self.button = None
        self.build()

    def activate_mission(self):
        if not self.is_available and not self.complete:
            self.is_available = True

    def set_reward_multiplier(self):
        self.reward_multiplier = self.level + 1
    
    def get_required_vault_balance(self):
        return get_vault_balance_requirement(self.level)
    
    def get_required_score(self):
        return get_score_requirement(self.level)
    
    def build(self):
        self.vault_balance_required = self.get_required_vault_balance()
        self.min_score = self.get_required_score()
        self.set_reward_multiplier()
        # comment this in for easy testing
        self.vault_balance_required = 0
        self.min_score = 12

    def check_completion(self, score, balance):
        return self.min_score <= score and self.vault_balance_required <= balance
    

class MissionManager:
    def __init__(self, number_of_missions):
        self.number_of_missions = number_of_missions
        self.missions:list[Mission] = self.create_missions()
        self.buttons = self.create_buttons()
        self.current_index = 0
        self.mission_and_button_list = []
        self.assign_buttons()
        self.setup_missions()

    def create_missions(self):
        return [Mission(i + 1) for i in range(self.number_of_missions)]
    
    def setup_missions(self):
        if self.missions:
            self.missions[0].activate_mission()

    def create_buttons(self):
        mission_buttons = []
        button_width = 200
        button_height = 50
        spacing = 70
        start_y = 150
        num_missions = self.number_of_missions

        for i in range(1, num_missions + 1):
            y = start_y + (i - 1) * spacing
            rect = Rect((WIDTH // 2 - button_width // 2, y), (button_width, button_height))
            mission_buttons.append((rect, i))
        return mission_buttons

    def assign_buttons(self):
        self.mission_and_button_list = list(zip(self.missions, self.buttons))

    def assign_mission_to_game(self, game, selected_mission):
        game.set_current_mission(selected_mission)

    def complete_mission(self, game):
        """Mark mission as complete and unlock the next one."""
        if game.do_mission_success() and not game.mission_success_handled:
            game.audio_manager.play_sound("win")
            game.mission_success_handled = True
            idx = self.missions.index(game.current_mission)
            if idx + 1 < len(self.missions):
                active_mission = self.missions[idx + 1]
                active_mission.activate_mission()
            return True
        return False
        

