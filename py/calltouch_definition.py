# -*- coding: utf-8 -*-

try:
	import urllib
	import json
	import datetime
	import requests
	import sys
	from io import BytesIO
except ImportError:
	sys.exit(
		'''Please install following packages using pip:
		urllib
		BytesIO
		'''
	)


class CalltouchApi:

	def __init__(self, config):

		self.config = config['calltouch']
		# config = {'calltouch': [{'siteId': 123, 'token': 'abcd', 'name': 'mynameis'},..]}
		self.url = 'http://api.calltouch.ru/calls-service/'

	def captureCalls(self, date, attribution, targetOnly, uniqOnly, uniqTargetOnly, callbackCall, rawData = False, untilEnd = False):

		""" Получение статистики по звонкам за один день в разрезе источника и кампании трафика с учетом типа звонка """

		global_res = []
		for cfg in self.config:
			query = {
				'clientApiId': cfg['token'],
				'dateFrom': date,
				'dateTo': date,
				'attribution': attribution,
				'targetOnly': targetOnly,
				'uniqueOnly': uniqOnly,
				'uniqTargetOnly': uniqTargetOnly,
				'callbackOnly': callbackCall
			}
			query = urllib.parse.urlencode(query)
			req = requests.get('{0}RestAPI/{1!s}/calls-diary/calls?{2!s}'.format(
				self.url,
				cfg['siteId'],
				query
				)
			)
			if(req.status_code == 200):
				response = json.loads(req.text)
				if rawData:
					campaigns_data = response
				else:
					campaigns = set([i['utmCampaign'] for i in response])
					campaigns_data = [
						{
							'date': date,
							'siteId': cfg['siteId'],
							'siteName': cfg['name'],
							'source': [i['utmSource'] for i in response if (i['utmCampaign'] == c)][0],
							'name': c, 
							'ordinaryCalls': len([o for o in response if (o['utmCampaign'] == c)]),
							'callIDs': [o['callId'] for o in response if (o['utmCampaign'] == c)],
							'uniqCalls': len([o for o in response if (o['utmCampaign'] == c and o['uniqueCall'] == 'True')]),
							'targetCalls': len([o for o in response if (o['utmCampaign'] == c and o['targetCall'] == 'True')]),
							'uniqTargetCalls': len([o for o in response if (o['utmCampaign'] == c and o['uniqTargetCall'] == 'True')])
						} 
					for c in campaigns]
				global_res += campaigns_data
			else:
				global_res += [{'siteId': cfg['siteId'], 'siteName': cfg['name'], 'date': date, 'errorCode': req.status_code, 'errorText': req.text}]
		if untilEnd:
			dateNext = datetime.datetime.strptime(date, '%d/%m/%Y').date() +  datetime.timedelta(1)
			if dateNext < datetime.date.today():
				global_res += self.captureCalls(dateNext.strftime('%d/%m/%Y'), attribution, targetOnly, uniqOnly, uniqTargetOnly, callbackCall, rawData, untilEnd)
		return global_res

	def captureRecords(self, node, callId):

		""" Скачивание записи звонка по его идентификатору """

		global_res = []
		for cfg in self.config:
			query = {
				'clientApiId': cfg['token']
			}
			query = urllib.parse.urlencode(query)
			req = requests.get('{0}/calls-service/RestAPI/{1!s}/calls-diary/calls/{2!s}/download?{3!s}'.format(
				node,
				cfg['siteId'],
				callId,
				query
				), 
				stream = True
			)
			if(req.status_code == 200):
				record = req.content;
				with open(str(callId) + '_record.mp3', 'wb') as r:
					r.write(record);
				global_res.append({'siteId': cfg['siteId'], 'siteName': cfg['name'], 'status': True, 'message': 'Call Record Saved as: ' + str(callId) + '_record.mp3'})
			else:
				global_res.append({'siteId': cfg['siteId'], 'siteName': cfg['name'], 'status': False, 'message': req.text, 'errorCode': req.status_code})
		return global_res

	def captureStats(self, dateStart, dateEnd, type = 'callsTotal'):

		""" Получение статистики для кабинета по предусмотренным в API срезам """
		
		global_res = []
		for cfg in self.config:
			query = {
				'access_token': cfg['token'],
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
			req = requests.get(self.url + '{0}RestAPI/statistics/{1!s}{2}{3}'.format(
				self.url,
				cfg['siteId'],
				req_chain,
				query)
			)
			if(req.status_code == 200):
				response = json.loads(req.text);
				if type == 'callsByDate':
					result = [{'date': k, 'siteId': cfg['siteId'], 'siteName': cfg['name'], 'calls': v} for k,v in response.items()]
				elif type == 'callsByDateSeoOnly':
					result = [{'date': k, 'siteId': cfg['siteId'], 'siteName': cfg['name'], 'calls': v} for k,v in response.items()]
				elif type == 'callsByKeywords':
					result = [{'keyword': k, 'siteId': cfg['siteId'], 'siteName': cfg['name'], 'calls': v} for k,v in response.items()]
				else:
					result = [{'siteId': cfg['siteId'], 'siteName': cfg['name'], 'callsTotal': response}]
				global_res += result
			else:
				global_res += [{'siteId': cfg['siteId'], 'siteName': cfg['name'], 'date': date, 'errorCode': req.status_code, 'errorText': req.text}]
		return global_res


