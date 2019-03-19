#coding=utf-8
#! /usr/bin/env python3

import argparse
import codecs
from console_logging import console
import json
import random
import os
import re
parser = argparse.ArgumentParser(description='Convert plain files to two-column format.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--input_f', help='input file')
parser.add_argument('--output', help='output folder')
args = parser.parse_args()

def get_json_data(fname):
	new_li = []
	with open(fname, 'r') as inputf:
		data_li = inputf.readlines()
		for line in set(data_li):
			line = line.strip()
			try:
				# print(line)
				line_data = json.loads(line)
				new_li.append(line_data)
			except:
				print(line)
				# console.error('line cannot be loaded as json')
			# break
	return new_li

def get_list(json_li):
	out_list = []
	words_list = [] # to remove duplicate sentences
	for i in xrange(len(json_li)): # for line in file
		try:
			line_li = []
			line_items = json_li[i]['items']
			text = re.sub(r'\s+|~|。|！|？|～|；', '', json_li[i]['text'].encode('utf-8').strip())
			# print('{}\t{}'.format(i, text))
			if text in words_list: 
				print(text)
				continue
			else:
				# print(text)
				words_list.append(text)
				# continue
			for j in xrange(len(line_items)): # for word in one sentence
				if line_items[j]['pos'] != '': desc = line_items[j]['pos']
				else: desc = line_items[j]['ne'] 
				for k in  xrange(len(line_items[j]['basic_words'])):
					if line_items[j]['basic_words'][k].isspace(): continue
					if k == 0: line_li.append(line_items[j]['basic_words'][k]+'	'+'B-'+desc+'	'+ 'O')
					elif k== len(line_items[j]['basic_words'])-1: line_li.append(line_items[j]['basic_words'][k]+'	'+'E-'+desc+'	'+ 'O')
					else: line_li.append(line_items[j]['basic_words'][k]+'	'+'I-'+desc+'	'+ 'O')
			out_list.append(line_li)
		except: print('get list has some problems!')
	return out_list

def save_data(fname, data_li):
	'''data_li is a list containing 50 sentences in which each word with the format word\tpos\O'''
	# print(len(data_li))
	with open(fname, 'w') as outputf:
	 	for line_li in data_li:
	 		for e in line_li: outputf.write('{}\n'.format(e.encode('utf-8')))
	 		outputf.write('\n')
	return 0

def split_fifty(data_li):
	split_li = []
	for i, line_li in enumerate(data_li):
		if i % 50 == 0 and i != 0: 
			if os.path.exists(args.output) == False: os.makedirs(args.output)
			outputfname = os.path.join(args.output, '{}.txt'.format(i/50))
			save_data(outputfname, split_li)
			split_li = []
		split_li.append(data_li[i])
	return 0

json_li = get_json_data(args.input_f)
print(len(json_li)) # 6739
data_li = get_list(json_li)
print(len(data_li)) # 54375
random.shuffle(data_li)
split_fifty(data_li)
