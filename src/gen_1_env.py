from gymnasium import Env, spaces

class PokemonGen1Env(Env):

    def __init__(self, config={}):
        self.debug = config.get("debug", False)

    def step(self, action):
        pass

    def reset(self, seed=None):
        pass

    def render(self):
        pass

    def close(self):
        pass

