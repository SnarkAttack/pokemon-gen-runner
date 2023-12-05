from .gen1_reward_tracker import Gen1RewardTracker

class BattleRewardTracker(Gen1RewardTracker):

    def __init__(self, poke_red):
        super().__init__()

    def update_reward(self, poke_red):

        reward = 0

        game_state = poke_red.get_game_state()

        if game_state.is_in_battle():
            print(game_state._battle_type)
        
        return reward