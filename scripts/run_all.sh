#!/bin/bash

for k in `ls generate_data*`
do	
	echo $k
	sbatch $k
done
