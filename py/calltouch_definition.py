# -*- coding: utf-8 -*-

try:
	import urllib
	import json
	import requests
	import sys
	from io import BytesIO
except ImportError:
	sys.exit(
		'''Please install following packages using pip:
		urllib
		json
		requests
		BytesIO
		'''
	)


class CalltouchApi:

	def __init__(self, siteId, token):

		self.siteId = siteId
		self.token = token
		self.url = 'http://api.calltouch.ru/calls-service/'

	def captureCalls(self,date, attribution, targetOnly, uniqTargetOnly, callbackCall):

		""" Получение статистики по звонкам за один день в разрезе источника и кампании трафика с учетом типа звонка """

		query = {
			'clientApiId': self.token,
			'dateFrom': date,
			'dateTo': date,
			'attribution': attribution,
			'targetOnly': targetOnly,
			'uniqTargetOnly': uniqTargetOnly,
			'callbackOnly': callbackCall
		}
		query = urllib.parse.urlencode(query)
		req = requests.get(self.url + 'RestAPI/' + str(self.siteId) + '/calls-diary/calls?' + query)
		if(req.status_code == 200):
			response = json.loads(req.text)
			campaigns = set([i['utmCampaign'] for i in response])
			campaigns_data = [
				{
					'date': date,
					'source': [i['utmSource'] for i in response if (i['utmCampaign'] == c)][0],
					'name': c, 
					'ordinaryCalls': len([o for o in response if (o['utmCampaign'] == c)]),
					'callIDs': [o['callId'] for o in response if (o['utmCampaign'] == c)],
					'uniqCalls': len([o for o in response if (o['utmCampaign'] == c and o['uniqueCall'] == 'True')]),
					'targetCalls': len([o for o in response if (o['utmCampaign'] == c and o['targetCall'] == 'True')]),
					'uniqTargetCalls': len([o for o in response if (o['utmCampaign'] == c and o['uniqTargetCall'] == 'True')])
				} 
			for c in campaigns]
			return campaigns_data
		else:
			return 'Server Responded With Status Code: ' + str(req.status_code)

	def captureRecords(self, node, callId):

		""" Скачивание записи звонка по его идентификатору """

		query = {
			'clientApiId': self.token
		}
		query = urllib.parse.urlencode(query)
		req = requests.get(node + '/calls-service/RestAPI/' + str(self.siteId) + '/calls-diary/calls/' + str(callId) + '/download?' + query, stream=True)
		if(req.status_code == 200):
			record = req.content;
			with open(str(callId) + '_record.mp3', 'wb') as r:
				r.write(record);
			return {'status': True, 'message': 'Call Record Saved as: ' + str(callId) + '_record.mp3'}
		else:
			return {'status': False, 'message': 'Server Responded With Status Code: ' + str(req.status_code)}

	def captureStats(self, dateStart, dateEnd, type = 'callsTotal'):

		""" Получение статистики для кабинета по предусмотренным в API срезам """

		query = {
			'access_token': self.token,
			'dateFrom': dateStart,
			'dateTo': dateEnd
		}
		query = urllib.parse.urlencode(query)
		req_chain = {
			'callsTotal': '/calls/total-count?',
			'callsByDate': '/calls/count-by-date?',
			'callsByDateSeoOnly': '/calls/seo/count-by-date?',
			'callsByKeywords': '/calls/seo/count-by-keywords?'
		}.get(type, '/calls/total-count?')
		req = requests.get(self.url + 'RestAPI/statistics/' + str(self.siteId) + req_chain + query)
		if(req.status_code == 200):
			response = json.loads(req.text);
			if type == 'callsByDate':
				result = [{'date': k, 'calls': v} for k,v in response.items()]
			elif type == 'callsByDateSeoOnly':
				result = [{'date': k, 'calls': v} for k,v in response.items()]
			elif type == 'callsByKeywords':
				result = [{'keyword': k, 'calls': v} for k,v in response.items()]
			else:
				result = {'callsTotal': response}
			return result
		else:
			return {'status': False, 'message': 'Server Responded With Status Code: ' + str(req.status_code)}


