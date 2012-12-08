try: import urllib.request as urllib2 #python 3.X
except ImportError: import urllib2
import urllib
import xml.etree.ElementTree as et

state = raw_input('Enter a State Abbreviation (2 letters): ')

parameters = {}
parameters['library'] = 'LocationInfo'
parameters['function'] = 'getCitiesInState'
parameters['state'] = state
parameters['apikey'] = 'baq3jbma7dc82f2rtkdwvt7w'

query = urllib.urlencode(parameters)
url = 'http://api.trulia.com/webservices.php?{}'.format(query)

def get_page(url):
    request = urllib2.urlopen(url) # open url
    response = str(request.read()) # read web page
    return response

page = get_page(url)
tree = et.fromstring(page)

for el in tree.findall('./response/LocationInfo/city'):	
	print 'Name:', el.find('name').text
	print 'Lat:', el.find('latitude').text
	print 'Lon:', el.find('longitude').text
	print ''