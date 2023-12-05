import uuid
import argparse
from pathlib import Path
from stable_baselines3 import PPO
from stable_baselines3.common.logger import TensorBoardOutputFormat
from stable_baselines3.common.callbacks import BaseCallback, CheckpointCallback, EveryNTimesteps
from pokemon_gen_runner.environments import PokemonGen1Env

class BestScoreCallback(BaseCallback):

    def __init__(self, verbose=False):
        super().__init__(verbose)

    def _on_training_start(self):
        output_formats = self.logger.output_formats
        # Save reference to tensorboard formatter object
        # note: the failure case (not formatter found) is not handled here, should be done with try/except.
        self.tb_formatter = next(formatter for formatter in output_formats if isinstance(formatter, TensorBoardOutputFormat))

    def _on_step(self):
        best_score = self.training_env.unwrapped.get_attr("best_reward")[0]
        self.logger.record("rollout/best_reward", best_score)
        return True

def train(max_steps, num_epochs, verbose=False, headless=False):

    session_id = str(uuid.uuid4())[:8]
    session_path = Path(f"output/{session_id}")
    tensorboard_path = Path(f"tensorboard")
    model_path = Path(f"models/{session_id}.zip")

    checkpoint_callback = CheckpointCallback(save_freq=max_steps, save_path=session_path,
                                     name_prefix='pg1')
    
    best_score_callback = BestScoreCallback()
    best_score_logger_callback = EveryNTimesteps(n_steps=max_steps, callback=best_score_callback)

    env_config = {
        'rom_path': 'rom/PokemonRed.gb',
        'init_state': 'game_states/base.state',
        'max_steps': max_steps,
        'headless': headless
    }

    env = PokemonGen1Env(env_config)

    model = PPO('MultiInputPolicy',
                env,
                n_steps=max_steps,
                n_epochs=num_epochs,
                batch_size=max_steps,
                tensorboard_log=tensorboard_path,
                verbose=verbose,
            )

    model.learn(total_timesteps=max_steps*num_epochs,
                callback=[checkpoint_callback, best_score_logger_callback],
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