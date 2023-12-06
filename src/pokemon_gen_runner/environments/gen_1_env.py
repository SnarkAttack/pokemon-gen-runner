import numpy as np
import gymnasium as gym
from gymnasium.spaces import Discrete
from pyboy import PyBoy
from gymnasium.spaces import Box, Dict
from ..action import ALL_VALID_ACTIONS
from ..reward_trackers import TouchGrassRewardTracker, BattleRewardTracker, ExplorerRewardTracker
from ..observation_manager import ScreenOnlyObservationManager

class PokemonGen1Env(gym.Env):
    def __init__(self, config={}):
        # Required config arguments
        self._rom_path = config['rom_path']
        self._init_state = config['init_state']
        self._max_steps = config['max_steps']
        self._reward_tracker_type = config['reward_tracker_type']

        # Optional config arguments
        self._debug = config.get("debug", False)
        self._seed = config.get('seed', None)

        head = 'headless' if config.get('headless', False) else 'SDL2'
        
        self._pyboy = PyBoy(
            self._rom_path,
            game_wrapper=True,
            window_type=head
        )

        self._poke_red = self._pyboy.game_wrapper()
        self._poke_red.start_game()

        self._observation_manager = ScreenOnlyObservationManager()

        self._steps = 0
        self._reward_tracker = self._get_new_reward_tracker()

        # 8 options: up, down, left, right, A, B, Start, Select
        self.action_space = Discrete(len(ALL_VALID_ACTIONS))
        self.observation_space = self._observation_manager.observation_space

        with open(self._init_state, 'rb') as f:
            self._pyboy.load_state(f)

        if not head == 'headless':
            self._pyboy.set_emulation_speed(4)

        self.reset()

    def _get_new_reward_tracker(self):
        if self._reward_tracker_type == 'touch_grass':
            return TouchGrassRewardTracker()
        elif self._reward_tracker_type == 'battle':
            return BattleRewardTracker()
        elif self._reward_tracker_type == 'explore':
            return ExplorerRewardTracker()
        else:
            raise ValueError(f"{self._reward_tracker_type} is not a valid reward tracker id")

    def _check_if_finished(self):
        return self._steps >= self._max_steps
    
    def get_total_reward(self):
        return self._reward_tracker.total_reward

    def step(self, action):

        action = ALL_VALID_ACTIONS[action]

        action.perform_action(self._pyboy)

        reward = self._reward_tracker.get_reward(self._poke_red)

        self._steps += 1

        terminated = self._check_if_finished()

        observation = self._observation_manager.current_observation(self._poke_red)

        return observation, reward, False, terminated, {}

    def reset(self, seed=None):

        self.run_results = self._reward_tracker.report_results()

        with open(self._init_state, 'rb') as f:
            self._pyboy.load_state(f)

        self._steps = 0
        self._reward_tracker = self._get_new_reward_tracker()
        
        observation = self._observation_manager.current_observation(self._poke_red)

        return observation, {}

    def render(self):
        game_pixels_render = self.screen.screen_ndarray() # (144, 160, 3)
        return game_pixels_render

    def close(self):
        pass



