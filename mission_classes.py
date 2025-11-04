from sandbox import get_score_requirement, get_vault_balance_requirement

class Mission:
    def __init__(self, level):
        self.level = level
        self.vault_balance_required = 0
        self.min_score = 0
        self.reward_multiplier = 0.0

    def set_reward_multiplier(self):
        self.reward_multiplier = 0.5*self.level
    
    def get_required_vault_balance(self):
        return get_vault_balance_requirement(self.level)
    
    def get_required_score(self):
        return get_score_requirement(self.level)
    
    def build(self):
        self.vault_balance_required = self.get_required_vault_balance()
        self.min_score = self.get_required_score()
        self.set_reward_multiplier()
    

    
# multipliers go up by 0.5 with each stage: 0.5x -> 1.0x -> 1.5
# required balance starts at 50 and goes up exponentially
# required score starts at 100 and goes up at a steeper rate

