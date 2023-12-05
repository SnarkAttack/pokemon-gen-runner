import gymnasium as gym
from gymnasium.spaces import Dict, Discrete, Box
from gymnasium.wrappers import FlattenObservation
import pyboy.plugins.game_wrapper_pokemon_gen1 as poke_gen_1
from pyboy import PyBoy, WindowEvent
from ..action import ALL_VALID_ACTIONS
from ..reward_trackers.gen1_reward_tracker import FindGrassRewardTracker

class PokemonGen1Env(gym.Env):
    def __init__(self, config={}):
        # Required config arguments
        self._rom_path = config['rom_path']
        self._init_state = config['init_state']
        self._max_steps = config['max_steps']

        # Optional config arguments
        self._debug = config.get("debug", False)
        self._seed = config.get('seed', None)

        # 8 options: up, down, left, right, A, B, Start, Select
        self.action_space = Discrete(len(ALL_VALID_ACTIONS))
        self.observation_space = Dict(
            {
                "map": Box(low=0, high=0x180, shape=(9, 10))
            }
        )

        head = 'headless' if config.get('headless', False) else 'SDL2'
        
        self._pyboy = PyBoy(
            self._rom_path,
            game_wrapper=True,
            window_type=head
        )

        self._poke_red = self._pyboy.game_wrapper()
        self._poke_red.start_game()

        self._steps = 0
        self._reward_tracker = FindGrassRewardTracker(self._poke_red)
        self.best_reward = 0

        with open(self._init_state, 'rb') as f:
            self._pyboy.load_state(f)

        if not head == 'headless':
            self._pyboy.set_emulation_speed(4)

        self.reset()

    def _check_if_finished(self):
        return self._steps >= self._max_steps

    def step(self, action):

        action = ALL_VALID_ACTIONS[action]
        # print(f"Steps: {self._steps}, action: {action.name}")
        action.perform_action(self._pyboy)

        new_map = self._poke_red._get_screen_background_tilemap()[::2, ::2]

        reward = self._reward_tracker.update_reward(self._poke_red)

        self._steps += 1

        terminated = self._check_if_finished()

        return {'map': new_map}, reward, False, terminated, {}

    def reset(self, seed=None):

        total_reward = self._reward_tracker._total_reward

        if total_reward > self.best_reward:
            self.best_reward = total_reward

        with open(self._init_state, 'rb') as f:
            self._pyboy.load_state(f)

        self._steps = 0
        self._reward_tracker = FindGrassRewardTracker(self._poke_red)

        start_map = self._poke_red._get_screen_background_tilemap()[::2, ::2]

        return {'map': start_map}, {}

    def render(self):
        return None

    def close(self):
        pass



