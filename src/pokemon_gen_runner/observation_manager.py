import numpy as np
from skimage.transform import resize
from gymnasium.spaces import Box, Dict

class ObservationManager():

    def __init__(self):
        pass

    @property
    def current_observation(self):
        return None

class ScreenOnlyObservationManager(ObservationManager):

    def __init__(self):
        super().__init__()
        self._output_screen_shape = (36, 40, 3)
        self._observation_space = Dict({
            'screen': Box(low=0, high=255, shape=self._output_screen_shape, dtype=np.uint8)
        })

    @property
    def observation_space(self):
        return self._observation_space

    def current_observation(self, poke_gen1):

        screen_array = poke_gen1.get_screen_array()

        observation = {
            'screen': (255*resize(screen_array, self._output_screen_shape)).astype(np.uint8)
        }
        
        return observation
