#! /usr/bin/env python3

'''this script is used for tokenization and pos tagging
baidu NLP api is used
pip install baidu-aip
'''
# import chardet
from aip import AipNlp
import json
import time

class Baiduapi():
	def tokpos_data(self, data_li):
		APP_ID = '10767475'
		API_KEY = 'LsxYY5WawstbGwu56DV4i8q1'
		SECRET_KEY = 'WoKhSGCfyDN8UbL22tpk2y0tseF9HKVz'
		client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
		new_data_json = []
		error = []
		print(len(data_li))
		for line in data_li:
			line = line.strip()
			time.sleep(1)
			try:
				result_json = client.lexer(line)
				result_json_str = json.dumps(result_json)
				print(result_json_str)
				new_data_json.append(result_json_str)
			except:
				error.append(line)
				continue
		return new_data_json, error

	# def jsontoli(self,new_data_json):

	
