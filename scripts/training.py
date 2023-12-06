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
            result_data = self.training_env.get_attr("run_results")
            avg_results = {}
            for k in result_data[0].keys():
                for result_dict in result_data:
                    avg_results[k] = avg_results.get(k, 0) + result_dict[k]
            for k, v in avg_results.items():
                avg_results[k] = v/len(result_data)
                self.logger.record(f"env_stats/avg_{k}", avg_results[k])
            # self.logger.record(f"env_stats/avg_reward", avg_reward)
        return True

def train(args):

    max_steps = args.max_steps
    num_epochs = args.num_epochs
    verbose = args.verbose
    headless = args.headless
    prev_save = args.prev_save
    num_cpus = args.num_cpus


    reward_tracker_type = 'explore'

    env_config = {
        'rom_path': 'rom/PokemonRed.gb',
        'init_state': 'game_states/base.state',
        'reward_tracker_type': reward_tracker_type,
        'max_steps': max_steps,
        'headless': headless
    }

    if num_cpus is None:
        if headless:
            num_cpus = multiprocessing.cpu_count()
        else:
            num_cpus = 1
    else:
        num_cpus = min(multiprocessing.cpu_count(), num_cpus)

    if num_cpus == 1:
        env = PokemonGen1Env(env_config)
    else:
        env = SubprocVecEnv([make_env(i, env_config) for i in range(num_cpus)])

    session_id = str(uuid.uuid4())[:8]
    session_id = f"{reward_tracker_type}_{session_id}"

    tensorboard_path = Path(f"tensorboard")
    session_path = Path(f"output/{session_id}")
    model_path = Path(f"output/{session_id}/model.zip")

    if prev_save is None:

        reset_num_timesteps = True

        model = PPO('MultiInputPolicy',
                    env,
                    n_steps=max_steps,
                    n_epochs=num_epochs,
                    batch_size=max_steps,
                    tensorboard_log=tensorboard_path,
                    verbose=verbose,
                    device=("cuda" if torch.cuda.is_available() else "cpu"),
                )
    else:
        if os.path.exists(prev_save):
            model = PPO.load(prev_save, env=env)
            model.n_steps = max_steps
            model.n_envs = num_cpus
            model.n_epochs = num_epochs
            model.rollout_buffer.buffer_size = max_steps
            model.rollout_buffer.n_envs = num_cpus
            model.rollout_buffer.reset()
            model.device = "cuda" if torch.cuda.is_available() else "cpu"

            reset_num_timesteps = False
        else:
            raise ValueError(f"{prev_save} does not exist.")

    checkpoint_callback = CheckpointCallback(save_freq=max_steps, save_path=session_path,
                                        name_prefix='pg1')
        
    tensorboard_callback = TensorboardCallback()

    print(f"Session id is {session_id}")

    model.learn(total_timesteps=max_steps*num_cpus*num_epochs,
                callback=[tensorboard_callback, checkpoint_callback],
                tb_log_name=session_id,
                progress_bar=True,
                reset_num_timesteps=reset_num_timesteps
               )
    
    model.save(model_path)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--max-steps', type=int)
    parser.add_argument('-n', '--num_epochs', type=int)
    parser.add_argument('-v', '--verbose', default=False, action='store_true')
    parser.add_argument('--headless', default=False, action='store_true')
    parser.add_argument('--num-cpus', type=int)
    parser.add_argument('--prev-save')

    args = parser.parse_args()

    train(args)