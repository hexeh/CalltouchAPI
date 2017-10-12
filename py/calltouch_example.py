# -*- coding: utf-8 -*-

import pprint
import json
import datetime

from calltouch_definition import CalltouchApi

if __name__ == '__main__':

	# config_file = open('configs/calltouch.json')
	# config = json.load(config_file)
	# config_file.close()

	config = {
		'calltouch': [
		{'name': 'Сайт №1', 'siteId': 1, 'token': 'aa'},
		{'name': 'Сайт №2', 'siteId': 2, 'token': 'bb'},
		{'name': 'Сайт №3', 'siteId': 3, 'token': 'cc'}
		]
	}
	stats_date = datetime.date.today() - datetime.timedelta(3)
	pp = pprint.PrettyPrinter(indent = 4)
	ct = CalltouchApi(config)

	""" Получение статистики по всем звонкам за указанную дату """

	call_stats_daily = ct.captureCalls(stats_date.strftime('%d/%m/%Y'), '1', 'false', 'false', 'false' , 'false', untilEnd = False)
	pp.pprint(call_stats_daily)

	""" Получение статистики по всем звонкам за указанную дату в сыром виде """

	call_stats_daily_raw = ct.captureCalls(stats_date.strftime('%d/%m/%Y'), '1', 'false', 'false', 'false' , 'false', rawData = True)
	pp.pprint(call_stats_daily_raw)

	""" Получение статистики по всем звонкам за диапазон дат от указанной до вчерашнего дня """

	call_stats = ct.captureCalls(stats_date.strftime('%d/%m/%Y'), '1', 'false', 'false', 'false' , 'false', untilEnd = True)
	with open('calltouch_calls_{0}_{1}.json'.format(stats_date.strftime('%d_%m_%Y'), (datetime.date.today() - datetime.timedelta(1)).strftime('%d_%m_%Y')), 'w') as f:
		json.dump(call_stats, f)

	""" Сохранение идентификаторов звонков за указанную ранее дату """

	totalCallIDs = [i['callIDs'] for i in call_stats]
	totalCallIDs = [y for x in totalCallIDs for y in x]

	""" Скачивание записей первых 5 звонков за указанную ранее дату 
		Получить адрес сервера можно в форме статьи - https://support.calltouch.ru/hc/ru/articles/209189625
	"""

	saveResults = [ct.captureRecords('PasteYourNodeAddressHere', i) for i in totalCallIDs[:4]]
	pp.pprint( saveResults )

	""" Получение статистики звонков по дням за указанный интервал дат """

	stats = ct.captureStats('11/07/2017', '11/07/2017', 'callsByDate')
	pp.pprint( stats )
