import numpy as np
from skimage.transform import resize
from gymnasium.spaces import Box, Dict
from .observation_manager import ObservationManager

class SingleScreenObservationManager(ObservationManager):

    def __init__(self):
        super().__init__()
        self._output_screen_shape = (36, 40, 3)
        self._observation_space = Dict({
            'screen': Box(low=0, high=255, shape=self._output_screen_shape, dtype=np.uint8)
        })

    def current_observation(self, poke_gen1):

        screen_array = poke_gen1.get_screen_array()

        observation = {
            'screen': (255*resize(screen_array, self._output_screen_shape)).astype(np.uint8)
        }
        
        return observation