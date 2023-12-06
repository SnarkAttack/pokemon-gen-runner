import numpy as np
from .gen1_reward_tracker import Gen1RewardTracker

class ExplorerRewardTracker(Gen1RewardTracker):

    def __init__(self):
        super().__init__()

    def get_reward(self, poke_gen1):

        reward = 0

        self._total_reward += reward
        
        return reward