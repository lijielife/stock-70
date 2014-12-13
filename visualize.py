# -*- coding: utf-8 -*-
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/config')

import MySQLdb
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import config

def main():
	connector = MySQLdb.connect(
		host    = config.db['host'],
		db      = config.db['db'],
		user    = config.db['user'],
		passwd  = config.db['passwd']
	)

	cursor = connector.cursor()

	date = []
	data = {
		'open': [],
		'high': [],
		'low': [],
		'close': []
	}
	volume = []

	argvs = sys.argv
	argc = len(argvs)

	# 企業コード
	ccode = "1301"
	if argc != 0:
		ccode = argvs[1]

	# 企業名を取得
	market = ""
	corp_name = ""
	cursor.execute("SELECT market,name FROM brands WHERE ccode = %s", [ccode])
	res = cursor.fetchall()
	for r in res:
		market = u"【" + unicode(r[0], 'utf-8') + u"】"
		corp_name = unicode(r[1], 'utf-8')

	# 株価を取得
	cursor.execute("SELECT date,open,high,low,close,volume FROM prices WHERE ccode = %s", [ccode])
	res = cursor.fetchall()
	for r in res:
		try:
			date.append(r[0].strftime("%Y-%m-%d"))
			data['open'].append(r[1])
			data['high'].append(r[2])
			data['low'].append(r[3])
			data['close'].append(r[4])
			volume.append(r[5])
		except:
			pass

	# 可視化
	fig, axes = plt.subplots(2,1)
	data_frame = pd.DataFrame(data, index=date)
	data_frame.plot(ax=axes[0], title=(market + corp_name))
	volume_series = pd.Series(volume, index=date)
	volume_series.plot(kind='bar', ax=axes[1])
	plt.show()

if __name__ == '__main__':
	main()
