from pygame import Rect
from constants import WIDTH
from sandbox import get_score_requirement, get_vault_balance_requirement

class Mission:
    def __init__(self, level):
        self.level = level
        self.vault_balance_required = 0
        self.min_score = 0
        self.reward_multiplier = 0.0
        self.complete = False
        self.is_available = False
        self.button = None
        self.build()

    def activate_mission(self):
        if not self.is_available and not self.complete:
            self.is_available = True

    def set_reward_multiplier(self):
        self.reward_multiplier = 0.5*self.level
    
    def get_required_vault_balance(self):
        return get_vault_balance_requirement(self.level)
    
    def get_required_score(self):
        return get_score_requirement(self.level)
    
    def build(self):
        # self.vault_balance_required = self.get_required_vault_balance()
        # self.min_score = self.get_required_score()
        self.set_reward_multiplier()
        self.vault_balance_required = 4
        self.min_score = 20

    def check_completion(self, score, balance):
        return self.min_score <= score and self.vault_balance_required <= balance
        return self.get_required_score() <= score and self.get_required_vault_balance() <= balance
    

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
        print(f"Starting Mission {selected_mission.level}", selected_mission.min_score)

    def complete_mission(self, game):
        """Mark mission as complete and unlock the next one."""
        if game.do_mission_success():
            print("availability:", game.current_mission.is_available, "completeness:", game.current_mission.complete)
            idx = self.missions.index(game.current_mission)
            if idx + 1 < len(self.missions):
                self.missions[idx + 1].activate_mission()
            return True
        return False
        
    
# multipliers go up by 0.5 with each stage: 0.5x -> 1.0x -> 1.5
# required balance starts at 50 and goes up exponentially
# required score starts at 100 and goes up at a steeper rate

