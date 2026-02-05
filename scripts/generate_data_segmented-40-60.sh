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


python create_db.py -b lmdb -s -r squash -c 3 -e jpg -C gzip -m lmdb/segmented-40-60/mean.binaryproto  lmdb/segmented-40-60/train.txt lmdb/segmented-40-60/train_db 256 256
python create_db.py -b lmdb -s -r squash -c 3 -e jpg -C gzip  lmdb/segmented-40-60/test.txt lmdb/segmented-40-60/test_db 256 256
