import numpy as np
from .gen1_reward_tracker import Gen1RewardTracker

class TouchGrassRewardTracker(Gen1RewardTracker):

    def __init__(self, poke_red, pyboy):
        super().__init__(poke_red, pyboy)
        self._total_reward = 0
        self._visited_tiles = np.zeros((0xF8, 45, 72))
        self._location = self._poke_red.get_player_location()

    def get_reward(self):

        reward = 0

        if self._location != self._poke_red.get_player_location():
            reward += 1

        if map[8,8] == 338:
            reward += 10

        self._total_reward += reward
        
        return reward