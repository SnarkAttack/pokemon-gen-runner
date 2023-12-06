class Gen1RewardTracker():

    def __init__(self):
        self._total_reward = 0

    @property
    def total_reward(self):
        return self._total_reward

    def get_reward(self, poke_gen1):
        raise NotImplementedError(f"update_reward not implemented for class {self.__class__.__name__}")
    
    def report_results(self):
        return {
            "total_reward": self._total_reward
        }