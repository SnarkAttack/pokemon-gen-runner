from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback
from pokemon_gen_runner.environments import PokemonGen1Env

if __name__ == "__main__":

    max_steps = 100

    checkpoint_callback = CheckpointCallback(save_freq=max_steps, save_path='output',
                                     name_prefix='pg1')

    env_config = {
        'rom_path': 'rom/PokemonRed.gb',
        'init_state': 'game_states/base.state',
        'max_steps': max_steps
    }

    env = PokemonGen1Env(env_config)

    model = PPO('MultiInputPolicy', env, n_steps=max_steps, batch_size=10, n_epochs=10, verbose=True)

    model.learn(total_timesteps=max_steps*10, callback=checkpoint_callback)