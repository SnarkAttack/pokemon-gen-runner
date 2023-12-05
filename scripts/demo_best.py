from pathlib import Path
import uuid
from pokemon_gen_runner.environments import PokemonGen1Env
from stable_baselines3 import PPO


def evaluate():
    max_steps = 2**23

    env_config = {
        'rom_path': 'rom/PokemonRed.gb',
        'init_state': 'game_states/base.state',
        'max_steps': max_steps,
    }
    
    num_cpu = 1 #64 #46  # Also sets the number of episodes per training iteration
    env = PokemonGen1Env(env_config)
    
    #env_checker.check_env(env)
    file_name = 'models/8277012b.zip'
    
    print('\nloading checkpoint')
    model = PPO.load(file_name, env=env)
        
    #keyboard.on_press_key("M", toggle_agent)
    obs, info = env.reset()
    while True:
        action, _states = model.predict(obs, deterministic=False)
        obs, rewards, terminated, truncated, info = env.step(action)
        if truncated:
            break
    env.close()

if __name__ == "__main__":
    evaluate()