import torch
import hydra
import os,sys
from rich import print_json
from omegaconf import OmegaConf

sys.path.append('..')


from bridge.runners.ipf import IPFSequential


# SETTING PARAMETERS

@hydra.main(config_path="./conf", config_name="config")
def main(args):
    print_json(data=OmegaConf.to_container(args))    # init lightning model

    print('Directory: ' + os.getcwd())
    ipf = IPFSequential(args)
    ipf.train()
    

if __name__ == '__main__':
    main()  
