from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
import json, httplib, urllib, datetime

def wave_admin(request):
    values = {}
    values["channels"] = get_channels_to_review()
    return render_to_response("admin.html", values, RequestContext(request))

def index(request):
    if request.method == 'POST':
    	handle_submitted_sponsored_post(request)
    values = {}
    values['name'] = "Will Jamieson"
    values['num_users'] = 10
    values['channels'] = get_active_channels()
    return render_to_response("index.html", values, RequestContext(request))

def settings(request):
    values = {}
    return render_to_response("settings.html", values, RequestContext(request))

"""
Helper Functions
"""

def get_channels_to_review():
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    params = urllib.urlencode({"where":json.dumps({
       "reviewed": False,
     })})
    connection.connect()
    connection.request('GET', '/1/classes/Channel?%s' % params, '', {
       "X-Parse-Application-Id": "zvIWkpNTutTz3MFfP4sa7WpzjoJ4bbxjRbc62FiW",
       "X-Parse-REST-API-Key": "5vaJiWwBd46tQaXQbBs75WHek4TrIONo6SWoYrhX"
     })
    result = json.loads(connection.getresponse().read())
    return [{"objectId": channel["objectId"], "name": channel["name"]} for channel in result["results"]]   

def get_active_channels():
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    params = urllib.urlencode({"where":json.dumps({
       "approved": True,
       "reviewed": True,
     })})
    connection.connect()
    connection.request('GET', '/1/classes/Channel?%s' % params, '', {
       "X-Parse-Application-Id": "zvIWkpNTutTz3MFfP4sa7WpzjoJ4bbxjRbc62FiW",
       "X-Parse-REST-API-Key": "5vaJiWwBd46tQaXQbBs75WHek4TrIONo6SWoYrhX"
     })
    result = json.loads(connection.getresponse().read())
    return [{"objectId": channel["objectId"], "name": channel["name"]} for channel in result["results"]]    

def save_sponsored_post(messageText, channel, latitude, longitude, radius, date):
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.request('POST', '/1/classes/Message', json.dumps({
       "user":  {
		  "__type": "Pointer",
		  "className": "_User",
		  "objectId": "Nn54Uqprw6" },
       "channel": {
           "__type": "Pointer",
           "className":"Channel",
           "objectId": channel,
       },
       "location":  {
           "latitude": latitude,
           "__type": "GeoPoint",
           "longitude": longitude
       },
       "date": {
           "__type": "Date",
           "iso": date.isoformat()
       },
       "promoted_radius" : radius,
       "messageText": messageText,
       "promoted": True,
     }), {
       "X-Parse-Application-Id": "zvIWkpNTutTz3MFfP4sa7WpzjoJ4bbxjRbc62FiW",
       "X-Parse-REST-API-Key": "5vaJiWwBd46tQaXQbBs75WHek4TrIONo6SWoYrhX",
       "Content-Type": "application/json"
     })
    result = json.loads(connection.getresponse().read())
    return result

def push_sponsored_post(messageText, channel, latitude, longitude, radius, date):
    import json,httplib
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.connect()
    connection.request('POST', '/1/push', json.dumps({
         "channels": [
           channel,
         ],
         "data": {
           "action": "com.greylock.wave.NEW_WAVE",
           "message": messageText,
           "lat": latitude,
           "long": longitude,
           "promotedRadius" : radius,
           "promoted" : True
         }, 
         "push_time": "{0}".format(date.isoformat()),
       }), {
         "X-Parse-Application-Id": "zvIWkpNTutTz3MFfP4sa7WpzjoJ4bbxjRbc62FiW",
         "X-Parse-REST-API-Key": "5vaJiWwBd46tQaXQbBs75WHek4TrIONo6SWoYrhX",
         "Content-Type": "application/json"
       })
    result = json.loads(connection.getresponse().read())
    print result

def get_num_users_in_radius(request, channel, latitude, longitude, radius):
    latitude = float(latitude)
    longitude = float(longitude)
    radius = float(radius)
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.connect()
    params = urllib.urlencode({"where":json.dumps({
       "currentLocation": {
         "$nearSphere": {
           "__type": "GeoPoint",
           "latitude": latitude,
           "longitude": longitude
         },
         "$maxDistanceInMiles": 10
       },
        "channels" : channel
     })})
    connection.request('GET', '/1/installations?%s' % params, '', {
       "X-Parse-Application-Id": "zvIWkpNTutTz3MFfP4sa7WpzjoJ4bbxjRbc62FiW",
       "X-Parse-Master-Key": "Y7YzCKJy5MhWUO2vHUE5IR8SIqxHEVQgmQILdxxZ"
     })
    result = json.loads(connection.getresponse().read())
    data = {"num_users": len(result["results"])}
    return HttpResponse(json.dumps(data))

def handle_submitted_sponsored_post(request):
	message = request.POST['message']
	latitude = float(request.POST['latitude'])
	longitude = float(request.POST['longitude'])
	radius = float(request.POST['radius'])
	channel = request.POST['channel']
	date = datetime.datetime.strptime(request.POST['datetime'],"%m/%d/%Y %H:%M")
	save_sponsored_post(message, channel, latitude, longitude, radius, date)
	# push_sponsored_post(message, channel, latitude, longitude, radius, date)