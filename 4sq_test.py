try: import urllib.request as urllib2 #python 3.X
except ImportError: import urllib2
import urllib
import json
import datetime

client_id = raw_input('Enter a Client ID: ')
secret = raw_input('Enter the Secret: ')
location = raw_input('Enter a Location: ')

parameters = {}
parameters['near'] = location
parameters['client_id'] = client_id
parameters['client_secret'] = secret
parameters['v'] = datetime.date.today().strftime('%Y%m%d')

query = urllib.urlencode(parameters)
url = 'https://api.foursquare.com/v2/venues/search?{}'.format(query)

def get_page(url):
    request = urllib2.urlopen(url) # open url
    response = str(request.read()) # read web page
    return response

page = get_page(url)
results = json.loads(page)

if results['meta']['code'] == 200:
	response = results['response']
	name = response['geocode']['feature']['displayName']
	lat = response['geocode']['feature']['geometry']['center']['lat']
	lng = response['geocode']['feature']['geometry']['center']['lng']
	print 'Lookup for location {} ({}, {})'.format(name, lat, lng)
	
	venues = response['venues']
	for venue in venues:
		try:
			print('Business Name: {}'.format(venue['name']))
			if venue.has_key('url'):
				print('URL: {}'.format(venue['url']))
			else:
				print('No URL available')
			print('Latitude: {}'.format(venue['location']['lat']))
			print('Longitude: {}'.format(venue['location']['lng']))
					
			tips_url = 'https://api.foursquare.com/v2/venues/{}/tips?{}'.format(venue['id'], query)
			tips_page = get_page(tips_url)
			tips_results = json.loads(tips_page)
			tip_count = tips_results['response']['tips']['count']
			print('# of Tips: {}'.format(tip_count))
			if tip_count > 0:
				print('Text of first review...')
				print('\t{}'.format(tips_results['response']['tips']['items'][0]['text']))
		except UnicodeEncodeError:
			print('Unable to parse ' + str(venue))
		print('')