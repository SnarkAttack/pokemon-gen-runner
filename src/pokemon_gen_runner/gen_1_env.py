from gymnasium import Env, spaces

class PokemonGen1Env(Env):

    def __init__(self, config={}):
        # Required config arguments
        self.rom_path = config['rom_path']

        # Optional config arguments
        self.debug = config.get("debug", False)



        # Gymnasium Env requirements

        # 8 options: left, right, up, down, A, B, Start, Select
        self.action_space = spaces.Discrete(8)

    def step(self, action):
        pass

    def reset(self, seed=None):
        pass

    def render(self):
        pass

    def close(self):
        pass



