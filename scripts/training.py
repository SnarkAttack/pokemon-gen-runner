import os
import uuid
import argparse
import torch
import multiprocessing
from pathlib import Path
from stable_baselines3 import PPO
from stable_baselines3.common.logger import TensorBoardOutputFormat
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv
from stable_baselines3.common.utils import set_random_seed
from stable_baselines3.common.callbacks import BaseCallback, CheckpointCallback, EveryNTimesteps
from pokemon_gen_runner.environments import PokemonGen1Env

def make_env(rank, env_conf, seed=0):
    """
    Utility function for multiprocessed env.
    :param env_id: (str) the environment ID
    :param num_env: (int) the number of environments you wish to have in subprocesses
    :param seed: (int) the initial seed for RNG
    :param rank: (int) index of the subprocess
    """
    def _init():
        env = PokemonGen1Env(env_conf)
        env.reset(seed=(seed + rank))
        return env
    set_random_seed(seed, using_cuda=torch.cuda.is_available())
    return _init


class TensorboardCallback(BaseCallback):

    def __init__(self, verbose=False):
        super().__init__(verbose)

    def _on_training_start(self):
        output_formats = self.logger.output_formats
        # Save reference to tensorboard formatter object
        # note: the failure case (not formatter found) is not handled here, should be done with try/except.
        self.tb_formatter = next(formatter for formatter in output_formats if isinstance(formatter, TensorBoardOutputFormat))

    def _on_step(self):
        if self.locals["dones"][0]:
            reward_trackers = [self.training_env.reset_infos[i]['reward_tracker'] for i in range(self.model.n_envs)]
            # self.logger.record(f"env_stats/avg_reward", avg_reward)
            rewards = [r._total_reward for r in reward_trackers]
            avg_reward = sum(rewards) / len(rewards)
            self.logger.record(f"env_stats/avg_reward", avg_reward)
        return True

def train(max_steps, num_epochs, verbose=False, headless=False):

    session_id = str(uuid.uuid4())[:8]
    session_path = Path(f"output/{session_id}")
    tensorboard_path = Path(f"tensorboard")
    model_path = Path(f"models/{session_id}.zip")

    checkpoint_callback = CheckpointCallback(save_freq=max_steps, save_path=session_path,
                                     name_prefix='pg1')
    
    tensorboard_callback = TensorboardCallback()

    env_config = {
        'rom_path': 'rom/PokemonRed.gb',
        'init_state': 'game_states/base.state',
        'reward_tracker_type': 'touch_grass',
        'max_steps': max_steps,
        'headless': headless
    }

    num_cpus = multiprocessing.cpu_count()

    if num_cpus == 1:
        env = PokemonGen1Env(env_config)
    else:
        env = SubprocVecEnv([make_env(i, env_config) for i in range(num_cpus)])

    file_name = "models/"

    if os.path.exists(file_name + '.zip'):
        model = PPO.load(file_name, env=env)
        model.n_steps = max_steps
        model.n_envs = num_cpus
        model.n_epochs = num_epochs
        model.rollout_buffer.buffer_size = max_steps
        model.rollout_buffer.n_envs = num_cpus
        model.rollout_buffer.reset()
    else:
        model = PPO('MultiInputPolicy',
                    env,
                    n_steps=max_steps,
                    n_epochs=num_epochs,
                    batch_size=max_steps,
                    tensorboard_log=tensorboard_path,
                    verbose=verbose,
                    device=("cuda" if torch.cuda.is_available() else "cpu"),
                )

    model.learn(total_timesteps=max_steps*num_cpus*num_epochs,
                callback=[tensorboard_callback, checkpoint_callback],
                tb_log_name=session_id,
                progress_bar=True
               )
    
    model.save(model_path)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--max-steps', type=int)
    parser.add_argument('-n', '--num_epochs', type=int)
    parser.add_argument('-v', '--verbose', default=False, action='store_true')
    parser.add_argument('--headless', default=False, action='store_true')

    args = parser.parse_args()

    train(args.max_steps, args.num_epochs, args.verbose, args.headless)