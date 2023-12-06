import numpy as np
from skimage.transform import resize
from gymnasium.spaces import Box, Dict
from .observation_manager import ObservationManager

class StackedScreenObservationManager(ObservationManager):

    def __init__(self, num_screens=3):
        super().__init__()
        self._num_screens = 3
        self._output_screen_shape = (36, 40, 3)
        self._observation_space = Dict({
            'screen_history': Box(low=0, high=255, shape=self._output_screen_shape, dtype=np.uint8)
        })

        self._screen_history = np.zeros(((self._num_screens,) + self._output_screen_shape))

    def current_observation(self, poke_gen1):

        screen_array = poke_gen1.get_screen_array()

        resized_screen = (255*resize(screen_array, self._output_screen_shape)).astype(np.uint8)

        np.roll(self._screen_history, 1, axis=0)

        self._screen_history[0] = resized_screen

        observation = {
            'screen_history': self._screen_history
        }
        
        return observation
