#!/usr/bin/env python



import glob
from PIL import Image

color_images = glob.glob("../raw/color/*/*")
#grayscale_images = glob.glob("../raw/grayscale/*/*")
#segmented_images = glob.glob("../raw/segmented/*/*")

#color_images = ['../raw/color/Tomato___Early_blight/0cd2270f-87f8-45b5-a4af-19fa34b2acaa___RS_Erly.B 9567.JPG', '../raw/color/Tomato___Early_blight/e701c578-1fa3-4ed3-9874-5f90c6d2eb3c___RS_Erly.B 9583.JPG', '../raw/color/Tomato___Early_blight/b06d301b-8cae-475a-9de3-80a42e908ae5___RS_Erly.B 9375.JPG', '../raw/color/Tomato___Early_blight/c7005da5-2322-44e9-aceb-c6abe348f98c___RS_Erly.B 6490.JPG', '../raw/color/Tomato___Early_blight/a52492e3-7916-4a13-a175-6a6c0dd3440a___RS_Erly.B 7613.JPG', '../raw/color/Tomato___Early_blight/c03bec63-8b1d-42ef-90d5-5dff0c2455ea___RS_Erly.B 9555.JPG', '../raw/color/Tomato___Early_blight/32e59188-5c46-4369-8991-5acfa253263b___RS_Erly.B 7781.JPG', '../raw/color/Tomato___Early_blight/d1668361-aac6-41e3-b729-c5e5092326c1___RS_Erly.B 7562.JPG', '../raw/color/Tomato___Early_blight/023fe2d4-6e1d-40ce-99ae-85ba90f436ff___RS_Erly.B 6354.JPG', '../raw/color/Tomato___Early_blight/b5c94157-7110-420f-99fc-040594d6ff12___RS_Erly.B 9474.JPG']

print color_images[:10]


import random
import os
import shutil

for x in range(20):
	_color = random.choice(color_images)
	_grayscale = _color.replace("/color/", "/grayscale/")
	_segmented = _color.replace(".JPG", "_final_masked.jpg").replace("/color/", "/segmented/")

	if os.path.exists(_color) and os.path.exists(_grayscale) and os.path.exists(_segmented):
		print _color
		print _grayscale
		print _segmented
		print "="*80
		_im = Image.open(_color)
		_im.save("img_"+str(x)+"_color.eps")
		_im = Image.open(_grayscale)
		_im.save("img_"+str(x)+"_grayscale.eps")
		_im = Image.open(_segmented)
		_im.save("img_"+str(x)+"_segmented.eps")
		#shutil.copy(_color, "img_"+str(x)+"_color.jpg")
		#shutil.copy(_grayscale, "img_"+str(x)+"_grayscale.jpg")
		#shutil.copy(_segmented, "img_"+str(x)+"_segmented.jpg")
		
	else:
		print _color
		print _grayscale
		print _segmented
		print "NONONONO"
		print "="*80

	
	
		
	
