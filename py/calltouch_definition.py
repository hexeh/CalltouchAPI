# -*- coding: utf-8 -*-

try:
	try:
	    from urllib.parse import urlencode
	except ImportError:
	    from urllib import urlencode
	import json
	import datetime
	import requests
	import sys
except ImportError:
	sys.exit(
		'''Please install following packages using pip:
		urllib
		json
		requests
		'''
	)


class CalltouchApi:

	def __init__(self, siteId, token, filtering = False):

		self.siteId = siteId
		self.token = token
		if filtering:
			self.filters = filtering
		else:
			self.filters = []
		node_detect = requests.get('https://api.calltouch.ru/calls-service/RestAPI/{0!s}/getnodeid/'.format(siteId))
		if node_detect.status_code == 200:
			node = json.loads(node_detect.text)
			self.node = 'https://api-node{0!s}.calltouch.ru/'.format(node['nodeId'])
		else:
			self.node = 'http://api.calltouch.ru/'
		self.url = self.node + 'calls-service/'

	def captureCalls(self, date, attribution = 1, targetOnly = False, uniqueOnly = False, uniqTargetOnly = False, callbackOnly = False, raw = False, debug = False, untilEnd = False):

		""" Получение статистики по звонкам за один день в разрезе источника и кампании трафика с учетом типа звонка """

		result = []
		if len(self.filters) > 0:
			for f in self.filters:
				query = {
					'clientApiId': self.token,
					'dateFrom': date,
					'dateTo': date,
					'attribution': attribution
				}
				if targetOnly:
					query['targetOnly'] = 'true'
				if uniqueOnly:
					query['targetOnly'] = 'true'
				if uniqTargetOnly:
					query['uniqTargetOnly'] = 'true'
				if callbackOnly:
					query['callbackOnly'] = 'true'
				for fk in f.keys():
					query[fk] = f[fk]
				query = urlencode(query)
				req = requests.get(self.url + 'RestAPI/' + str(self.siteId) + '/calls-diary/calls?' + query)
				if debug:
					print(self.url + 'RestAPI/' + str(self.siteId) + '/calls-diary/calls?' + query)
				if(req.status_code == 200):
					response = json.loads(req.text)
					campaigns = set([i['utmCampaign'] for i in response])
					if raw:
						result += response
					else:
						result += [
							{
								'date': date,
								'source': [i['source'] for i in response if (i['utmCampaign'] == c)][0],
								'medium': [i['medium'] for i in response if (i['utmCampaign'] == c)][0],
								'name': c, 
								'ordinaryCalls': len([o for o in response if (o['utmCampaign'] == c)]),
								'callIDs': [o['callId'] for o in response if (o['utmCampaign'] == c)],
								'uniqCalls': len([o for o in response if (o['utmCampaign'] == c and o['uniqueCall'] == 'True')]),
								'targetCalls': len([o for o in response if (o['utmCampaign'] == c and o['targetCall'] == 'True')]),
								'uniqTargetCalls': len([o for o in response if (o['utmCampaign'] == c and o['uniqTargetCall'] == 'True')])
							} 
						for c in campaigns]
				else:
					print('Server Responded With Status Code: ' + str(req.status_code))
		else:
			query = {
				'clientApiId': self.token,
				'dateFrom': date,
				'dateTo': date,
				'attribution': attribution
			}
			if targetOnly:
				query['targetOnly'] = 'true'
			if uniqueOnly:
				query['targetOnly'] = 'true'
			if uniqTargetOnly:
				query['uniqTargetOnly'] = 'true'
			if callbackOnly:
				query['callbackOnly'] = 'true'
			query = urlencode(query)
			req = requests.get(self.url + 'RestAPI/' + str(self.siteId) + '/calls-diary/calls?' + query)
			if debug:
				print(self.url + 'RestAPI/' + str(self.siteId) + '/calls-diary/calls?' + query)
			if(req.status_code == 200):
				response = json.loads(req.text)
				campaigns = set([i['utmCampaign'] for i in response])
				if raw:
					result += response
				else:
					result += [
						{
							'date': date,
							'source': [i['source'] for i in response if (i['utmCampaign'] == c)][0],
							'medium': [i['medium'] for i in response if (i['utmCampaign'] == c)][0],
							'name': c, 
							'ordinaryCalls': len([o for o in response if (o['utmCampaign'] == c)]),
							'callIDs': [o['callId'] for o in response if (o['utmCampaign'] == c)],
							'uniqCalls': len([o for o in response if (o['utmCampaign'] == c and o['uniqueCall'] == 'True')]),
							'targetCalls': len([o for o in response if (o['utmCampaign'] == c and o['targetCall'] == 'True')]),
							'uniqTargetCalls': len([o for o in response if (o['utmCampaign'] == c and o['uniqTargetCall'] == 'True')])
						} 
					for c in campaigns]
			else:
				print('Server Responded With Status Code: ' + str(req.status_code))
		if untilEnd:
			dateNext = datetime.datetime.strptime(date, '%d/%m/%Y').date() +  datetime.timedelta(1)
			if dateNext < datetime.date.today():
				result += self.captureCalls(dateNext.strftime('%d/%m/%Y'), attribution, targetOnly, uniqueOnly, uniqTargetOnly, callbackOnly, raw, debug, untilEnd)
		if debug:
			print(result)
		return(result)

	def captureRecords(self, callId):

		""" Скачивание записи звонка по его идентификатору """

		query = {
			'clientApiId': self.token
		}
		query = urlencode(query)
		req = requests.get(self.node + '/calls-service/RestAPI/' + str(self.siteId) + '/calls-diary/calls/' + str(callId) + '/download?' + query, stream=True)
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
		query = urlencode(query)
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
