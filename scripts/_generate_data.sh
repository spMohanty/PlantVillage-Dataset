#!/bin/bash

#SBATCH --workdir /home/mohanty/data/final_dataset
#SBATCH --nodes 1
#SBATCH --ntasks 1
#SBATCH --cpus-per-task 2
#SBATCH --mem 16384
#SBATCH --time 23:59:59
#SBATCH --partition gpu
#SBATCH --gres gpu:2
#SBATCH --qos gpu


module load caffe
echo STARTING AT `date`


