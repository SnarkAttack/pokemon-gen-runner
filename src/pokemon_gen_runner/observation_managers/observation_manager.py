import numpy as np
from skimage.transform import resize
from gymnasium.spaces import Box, Dict

class ObservationManager():

    def __init__(self):
        self._observation_space = None

    @property
    def observation_space(self):
        return self._observation_space

    @property
    def current_observation(self):
        return None
