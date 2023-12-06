import numpy as np
from .gen1_reward_tracker import Gen1RewardTracker

class ExplorerRewardTracker(Gen1RewardTracker):

    def __init__(self):
        super().__init__()
        self._location = (12, 12, 0) # Starting location

    def get_reward(self, poke_gen1):

        reward = 0

        location = poke_gen1.get_player_location()

        if self._location != location:
            reward += 1

        self._location = location

        self._total_reward += reward
        
        return reward