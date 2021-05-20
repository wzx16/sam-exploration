This code release accompanies the following paper:

### Spatial Action Maps Augmented with Visit Frequency Maps for Exploration Tasks

Zixing Wang, Nikolaos Papanikolopoulos

*(In submission) IROS 2021, Prague, Czech*

## Installation

We recommend using a [`conda`](https://docs.conda.io/en/latest/miniconda.html) environment for this codebase. The following commands will set up a new conda environment with the correct requirements (tested on Ubuntu 20.04 LTS):

```bash
# Create and activate new conda env and install packages
conda env create -n sam-exp --file=sam-exp.yml
conda activate sam-navi

# Install shortest path module (used in simulation environment)
cd spfa
python setup.py install
```

## Quickstart

We provide four pretrained policies, one for each test environment. Use `download-pretrained.sh` to download them:

```bash
./download-pretrained.sh
```

You can then use `enjoy.py` to run a trained policy in the simulation environment.

For example, to load the pretrained policy for `ST-COM`, you can run:

```bash
python enjoy.py --config-path logs/st-com-36000/config.yml
```

## Training in the Simulation Environment

The [`config`](config) directory contains template config files for all experiments in the paper. To start a training run, you can give one of the template config files to the `train.py` script. For example, the following will train a spatial action map with visit frequency map and sigmoid penalty policy:

```
python train.py config/opt-vfm-sam.yml
```

The training script will create a log directory and checkpoint directory for the new training run inside `logs/` and `checkpoints/`, respectively. Inside the log directory, it will also create a new config file called `config.yml`, which stores training run config variables and can be used to resume training or to load a trained policy for evaluation.

### Config Files
 
config/st-com.yml (steering commands),  
config/sam.yml (spatial action map),  
config/vfm-sam.yml (spatial action map with visit frequency map, SAM-VFM (B)).  
config/opt-vfm-sam.yml (spatial action map with visit frequency map and sigmoid penalty, SAM-VFM (A)). 

### Simulation Environment

To explore the simulation environment using our proposed dense action space (spatial action maps), you can use the `tools_click_agent.py` script, which will allow you to click on the local overhead map to select actions and move around in the environment.

```bash
python tools_click_agent.py
```

### Evaluation

Trained policies can be evaluated using the `evaluate.py` script, which takes in the config path for the training run. For example, to evaluate the SAM-VFM (B) pretrained policy, you can run:

```
python evaluate.py --config-path logs/vfm-sam-36000/config.yml
```

This will load the trained policy from the specified training run, and run evaluation on it. The results are saved to an `.npy` file in the `eval` directory. You can then modify the visualize.py to open the .npy file and visualize it.

## Acknowledgement

We'd like to thank the authors of the paper [**Spatial Action Maps for Manipulation**](https://spatial-action-maps.cs.princeton.edu/) for sharing codes. Please visit their project page for more information.
