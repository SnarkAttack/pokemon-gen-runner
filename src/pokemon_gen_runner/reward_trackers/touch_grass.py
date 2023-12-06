import numpy as np
from .gen1_reward_tracker import Gen1RewardTracker

class TouchGrassRewardTracker(Gen1RewardTracker):

    def __init__(self):
        super().__init__()
        self._total_reward = 0
        self._visited_tiles = np.zeros((0xF8, 45, 72))