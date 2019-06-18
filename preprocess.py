import json 
import csv
import pandas as pd

def json_to_csv(from_file, to_file, this_month):
	# 打开json文件
	with open(from_file) as json_file:
		# 以写的方式打开csv文件
		with open (to_file, 'w') as csv_file:
			fieldnames = ['url', 'city', 'new_num', 'rent']
			writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
			writer.writerow({'url':'url', 'city':'city', 'new_num':'num', 'rent':this_month})

			for line in json_file:
				# 按行将json数据转化为字典
				dic = json.loads(line)
				# 替换数字中间的逗号
				dic['new_num'] = dic['new_num'].replace(',', '')
				dic['rent'] = dic['rent'].replace(',', '') 
				if dic['new_num'] == '--':
					dic['new_num'] = ''
				if dic['rent'] == '--':
					dic['rent'] = ''
				# 写入csv文件
				writer.writerow(dic)

# 选列、nan
def preprocess(from_file, to_file, this_month):
	df = pd.read_csv(from_file, usecols = ['city', this_month], na_values = 'na')
	if from_file == 'mid_rent.csv':
		df = df.fillna(0)
	df.to_csv(to_file, index = False)
