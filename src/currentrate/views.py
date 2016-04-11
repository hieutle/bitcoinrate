from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from pubnub import Pubnub

import urllib, json
import time 

CHANNEL = 'Current Rate'

# Create your views here.

def get_rate():
	url = "http://api.coindesk.com/v1/bpi/currentprice.json"
	response  = urllib.urlopen(url)
	data = json.loads(response.read())

	return data['bpi']['USD']['rate'], data['bpi']['EUR']['rate'], data['time']['updated']

def index(request):
	while True:
		a,b,c = get_rate()
		context = {'USD Rate' : a,
					'EUR Rate' : b,
					'updated time' : c,
					'notification_channel' : CHANNEL,
					'subkey' : 'demo',
					}
		print a + "---" + b
		time.sleep(3)
	return render(request, 'index2.html', context)
	# return HttpResponse("Current Price")


def publish_rate():	
	pubnub = Pubnub(publish_key='demo', subscribe_key='demo', ssl_on=False)
	info = pubnub.publish(channel=CHANNEL, message=get_rate())
