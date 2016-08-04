#!/bin/bash


for _config in `ls lmdb`
do
	echo lmdb/$_config
	cp _generate_data.sh generate_data_$_config.sh
	echo "python create_db.py -b lmdb -s -r squash -c 3 -e jpg -C gzip -m lmdb/$_config/mean.binaryproto  lmdb/$_config/train.txt lmdb/$_config/train_db 256 256" >> generate_data_$_config.sh
	echo "python create_db.py -b lmdb -s -r squash -c 3 -e jpg -C gzip  lmdb/$_config/test.txt lmdb/$_config/test_db 256 256" >> generate_data_$_config.sh
done
