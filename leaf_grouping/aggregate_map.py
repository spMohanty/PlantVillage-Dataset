#!/usr/bin/env python


import glob
import csv


MAP = {}
for _csvfile in glob.glob("filtered_leafmaps/*.csv"):
	csvfile = open(_csvfile, "r")
	reader = csv.DictReader(csvfile)
	#  42520 ['File Name', 'Leaf #']
	_key = _csvfile.split("/")[-1].split(".")[0]
	for row in reader:
		_filename = ".".join(row['File Name'].split(".")[:-1])
		_leaf_id = row['Leaf #']

		_leaf_id = _key+":::"+_leaf_id

		_filename = _filename.lower().strip()

		try:
			MAP[_filename].append(_leaf_id)
		except:
			MAP[_filename] = [_leaf_id]


for _key in MAP.keys():
	if len(MAP[_key])>1:
		print _key, " ------ ", MAP[_key]


import json

f=open("leaf-map.json", "w")
f.write(json.dumps(MAP))
f.close()
