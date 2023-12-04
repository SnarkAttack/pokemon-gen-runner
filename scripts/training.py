import uuid
from pathlib import Path
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback
from pokemon_gen_runner.environments import PokemonGen1Env

if __name__ == "__main__":

    max_steps = 100
    num_epochs = 10

    session_id = str(uuid.uuid4())[:8]
    session_path = Path(f"output/{session_id}")
    tensorboard_path = Path(f"tensorboard")

    checkpoint_callback = CheckpointCallback(save_freq=max_steps, save_path=session_path,
                                     name_prefix='pg1')

    env_config = {
        'rom_path': 'rom/PokemonRed.gb',
        'init_state': 'game_states/base.state',
        'max_steps': max_steps
    }

    env = PokemonGen1Env(env_config)

    model = PPO('MultiInputPolicy', env, n_steps=max_steps, n_epochs=num_epochs, batch_size=max_steps, verbose=True, tensorboard_log=tensorboard_path)

    model.learn(total_timesteps=max_steps*num_epochs, callback=checkpoint_callback, tb_log_name=session_id)