

class Gen1RewardTracker():

    def __init__(self):
        self._total_reward = 0

    def initialize(self, poke_red):
        raise NotImplementedError(f"initialize not implemented for class {self.__class__.__name__}")

    def update_reward(self, poke_red):
        raise NotImplementedError(f"update_reward not implemented for class {self.__class__.__name__}")
    

class FindGrassRewardTracker(Gen1RewardTracker):

    def __init__(self, poke_red):
        super().__init__()
        self._location = poke_red.get_player_location()

    def update_reward(self, poke_red):
        map = poke_red._get_screen_background_tilemap()[::2, ::2]
        location = poke_red.get_player_location()

        reward = 0

        if location != self._location:
            reward += 1

        self._location = location

        if map[4,4] == 338:
            reward += 10

        self._total_reward += reward
        
        return reward