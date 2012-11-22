"""
Requests a location from standard input.
Prints out nearby businesses from the Yelp API, and then the fulltext of the first review scraped from the URL.
"""

from yelp import ReviewSearchApi

import re
try: import urllib.request as urllib2 #python 3.X
except ImportError: import urllib2

key = raw_input('Enter an API Key: ')
location = raw_input('Enter a location: ')

results = ReviewSearchApi(client_key=key, output="json").by_location(location, term='', radius=1)

def get_page(url):
    request = urllib2.urlopen(url) # open url
    response = str(request.read()) # read web page
    return response

review_count_pattern = '(\d*)\sReview'
review_pattern = 'review_comment.*?>(.*?)</p'
	
if (results['message']['text'] == 'OK'):
	for result in results['businesses']:
		print('Business Name: {}'.format(result['name']))
		print('URL: {}'.format(result['url']))
		print('Latitude: {}'.format(result['latitude']))
		print('Longitude: {}'.format(result['longitude']))
		print('# Reviews via API: {}'.format(len(result['reviews'])))
		
		page = get_page(result['url'])
		matches = re.search(review_count_pattern, page, re.DOTALL)
		if matches:
			review_count = matches.group(1)
			print('# Reviews via URL: {}'.format(review_count))
						
			matches = re.search(review_pattern, page, re.DOTALL)
			if matches:
				print('Text of first review...')
				print('\t{}'.format(matches.group(1).replace('<br>', '\n\t')))
		
		print('')