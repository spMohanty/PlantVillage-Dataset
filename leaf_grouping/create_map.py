#!/usr/bin/env python


# -*- coding: utf-8 -*-
import xlrd
import csv
from os import sys
import glob

def csv_from_excel(excel_file, target_prefix):
    workbook = xlrd.open_workbook(excel_file)
    all_worksheets = workbook.sheet_names()
    for worksheet_name in all_worksheets:
        worksheet = workbook.sheet_by_name(worksheet_name)
        your_csv_file = open(target_prefix+"_"+''.join([worksheet_name,'.csv']), 'wb')
        wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

        for rownum in xrange(worksheet.nrows):
            wr.writerow([unicode(entry).encode("utf-8") for entry in worksheet.row_values(rownum)])
        your_csv_file.close()


for _file in glob.glob("leaf_maps/*"):
	print _file
	
	csv_from_excel(_file, _file.replace(" Leaf Counts.xlsx",""))
