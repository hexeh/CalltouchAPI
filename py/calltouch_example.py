# -*- coding: utf-8 -*-

import pprint
from calltouch_definition import CalltouchApi

if __name__ == '__main__':

	ct = CalltouchApi('PasteYourSiteIdHere', 'PasteYourTokenHere')
	pp = pprint.PrettyPrinter( indent = 4 )

	""" Получение статистики по всем звонкам за указанную дату """
	result = ct.captureCalls( '11/07/2017', '1', 'false', 'false', 'false' )
	pp.pprint( result )

	""" Сохранение идентификаторов звонков за указанную ранее дату """

	totalCallIDs = [i['callIDs'] for i in result]
	totalCallIDs = [y for x in totalCallIDs for y in x]

	""" Скачивание записей первых 5 звонков за указанную ранее дату 
		Получить адрес сервера можно в форме статьи - https://support.calltouch.ru/hc/ru/articles/209189625
	"""
	saveResults = [ct.captureRecords('PasteYourNodeAddressHere', i) for i in totalCallIDs[:5]]
	pp.pprint( saveResults )

	""" Получение статистики звонков по дням за указанный интервал дат """

	stats = ct.captureStats('11/07/2017', '11/07/2017', 'callsByDate')
	pp.pprint( stats )