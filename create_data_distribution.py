#!/usr/bin/env python

import glob
import json
import random
import numpy as np
import os
import math

leaf_map = json.loads(open("leaf-map.json", "r").read())


INPUT_FOLDER = "./raw"
OUTPUT_FOLDER = "./lmdb"

TRAIN_PERCENT = 80


def determine_leaf_group(leaf_identifier, className):
	global leaf_map
		
	try:
		foo = leaf_map[leaf_identifier.lower().strip()]
		if len(foo) == 1:
			return foo[0]
		else:
			for _suggestion in foo:
				if _suggestion.find(className) != -1:
					return _suggestion
			return str(random.randint(1,10000000000000000000000))
	except:
		return str(random.randint(1,10000000000000000000000))

def compute_per_class_distribution(DATASET):
	classMap = {}
	count = 0
	for datum in DATASET:
		try:
			classMap[datum[1]].append(datum[0])
			count += 1
		except:
			classMap[datum[1]] = [datum[0]]
			count += 1
	for _key in classMap:
		classMap[_key] = len(classMap[_key]) 

	return classMap

def distribute_buckets(BUCKETS, train_probability):
	train = []
	test = []
	
	for _key in BUCKETS.keys():
		bucket = BUCKETS[_key]

		if random.random() <= train_probability:
			train += bucket
		else:
			test += bucket	
	return train, test	


for data_type in glob.glob(INPUT_FOLDER +"/*"):
	
	data_type_name = data_type.split("/")[-1]	
	print data_type_name

	BUCKETS = {}
	all_images = glob.glob(data_type+"/*/*")
	for _img in all_images:
		image_name = _img.split("/")[-1]
		className = _img.split("/")[-2]
		#Check if the image belongs to a particular known group
		image_identifier = image_name.replace("_final_masked","")
		image_identifier = image_identifier.split("___")[-1]	
		image_identifier = image_identifier.split("copy")[0].replace(".jpg", "").replace(".JPG","").replace(".png","").replace(".PNG", "")

		#print "\"",image_identifier,"\"", className			
		#print image_name, "======================>", determine_leaf_group(image_identifier, className)
		group = determine_leaf_group(image_identifier, className)
		try:
			BUCKETS[group].append((_img, className))
		except:
			BUCKETS[group] = [(_img, className)]
	
	train_probs = [0.2, 0.4, 0.5, 0.6, 0.8]
	for train_prob in train_probs:	
		CANDIDATE_DISTRIBUTIONS = []
		CANDIDATE_VARIANCES = []
		for k in range(1000):
			#print "======================="
			#print "K ::",k
			train, test = distribute_buckets(BUCKETS, train_prob)
			train_dist = compute_per_class_distribution(train) 
			test_dist =  compute_per_class_distribution(test) 
			spread_data = []
			for _key in train_dist:
				#print _key, train_dist[_key] * 1.0 /(train_dist[_key]+test_dist[_key])
				spread_data.append(train_dist[_key] * 1.0 /(train_dist[_key]+test_dist[_key]))

			CANDIDATE_DISTRIBUTIONS.append((train, test))
			CANDIDATE_VARIANCES.append(np.var(spread_data))

			#print "Train : ", len(train)
			#print "Test : ", len(test)


		train, test = CANDIDATE_DISTRIBUTIONS[np.argmax(CANDIDATE_VARIANCES)]
		print len(train)
		print len(test)
		
		train_dist = compute_per_class_distribution(train)
		test_dist =  compute_per_class_distribution(test)
		spread_data = []
		for _key in train_dist:
			print _key, train_dist[_key] * 1.0 /(train_dist[_key]+test_dist[_key])
			spread_data.append(train_dist[_key] * 1.0 /(train_dist[_key]+test_dist[_key]))

		print "Mean :: ", np.mean(spread_data)
		print "Variance: ", np.var(spread_data)
		
		target_folder_name = data_type_name + "-" + str(int(math.ceil(train_prob*100)))+"-"+str(int(math.ceil((1-train_prob)*100)))

		try:
			os.mkdir(OUTPUT_FOLDER+"/"+target_folder_name)
		except:
			pass

		labels_map = {}
		for _entry in train:
			try:
				labels_map[_entry[1]] += 1
			except:
				labels_map[_entry[1]] = 1
		print labels_map
		labels_list = sorted(labels_map.keys())

		f = open(OUTPUT_FOLDER+"/"+target_folder_name+"/train.txt","w")
		train_txt = ""
		for _entry in train:
			train_txt += os.path.abspath(_entry[0])+"\t"+str(labels_list.index(_entry[1]))+"\n"
		f.write(train_txt)
		f.close()

		f = open(OUTPUT_FOLDER+"/"+target_folder_name+"/test.txt","w")
		test_txt = ""
		for _entry in test:
			test_txt += os.path.abspath(_entry[0])+"\t"+str(labels_list.index(_entry[1]))+"\n"
		f.write(test_txt)
		f.close()
	
		f = open(OUTPUT_FOLDER+"/"+target_folder_name+"/labels.txt","w")
		f.write("\n".join(labels_list))
		f.close()
	#break
