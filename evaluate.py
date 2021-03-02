# Prevent numpy from using up all cpu
import os
os.environ['MKL_NUM_THREADS'] = '1'  # pylint: disable=wrong-import-position
import argparse
from pathlib import Path
import numpy as np
import utils
import time

def _run_eval(cfg, num_episodes=200):
    env = utils.get_env_from_cfg(cfg, random_seed=9)
    policy = utils.get_policy_from_cfg(cfg, env.get_action_space(), random_seed=9)
    data = [[] for _ in range(num_episodes)]
    episode_count = 0
    state = env.reset()
    start_time = time.time()
    end_time = time.time()
    while True:
        action, _ = policy.step(state)
        state, _, done, info = env.step(action)
        end_time = time.time()
        data[episode_count].append({'cube_found': info['cube_found'],\
                                    'cumulative_distance': info['cumulative_distance'],\
                                    'explored_area': info['explored_area'],\
                                    'repetitive_exploration_rate': info['repetive_exploration_rate']})
        
        time_elasped = end_time - start_time
        if done or time_elasped > 600:
            state = env.reset()
            start_time = time.time()
            episode_count += 1
            if done:
                print('Completed {}/{} episodes'.format(episode_count, num_episodes))
            if time_elasped > 600:
                print('Failed to complete episode:', episode_count)
                data[episode_count].append({'cube_found': done,\
                                    'cumulative_distance': info['cumulative_distance'],\
                                    'explored_area': info['explored_area'],\
                                    'repetitive_exploration_rate': info['repetive_exploration_rate']})
            if episode_count >= num_episodes:
                break
    return data

def main(args):
    config_path = args.config_path
    if config_path is None:
        config_path = utils.select_run()
    if config_path is None:
        print('Please provide a config path')
        return
    cfg = utils.read_config(config_path)

    eval_dir = Path(cfg.logs_dir).parent / 'eval'
    if not eval_dir.exists():
        eval_dir.mkdir(parents=True, exist_ok=True)

    eval_path = eval_dir / '{}.npy'.format(cfg.run_name)
    data = _run_eval(cfg)
    np.save(eval_path, data)
    print(eval_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config-path')
    main(parser.parse_args())
