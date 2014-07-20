from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
import json, httplib, urllib, datetime

def wave_admin(request):
    values = {}
    values["channels"] = get_channels_to_review()
    return render_to_response("admin.html", values, RequestContext(request))

def index(request):
    values = {}
    values['name'] = "Will Jamieson"
    values['num_users'] = 10
    return render_to_response("index.html", values, RequestContext(request))

def settings(request):
    values = {}
    return render_to_response("settings.html", values, RequestContext(request))

"""
Helper Functions
"""
def

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

def submit_sponsored_post(messageText, channel, latitude, longitude, date):
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
       "messageText": messageText,
       "promoted": True,
     }), {
       "X-Parse-Application-Id": "zvIWkpNTutTz3MFfP4sa7WpzjoJ4bbxjRbc62FiW",
       "X-Parse-REST-API-Key": "5vaJiWwBd46tQaXQbBs75WHek4TrIONo6SWoYrhX",
       "Content-Type": "application/json"
     })
    result = json.loads(connection.getresponse().read())
    return result

# def get_num_users_in_radius(channel, latitude, longitude, radius):
#     connection = httplib.HTTPSConnection('api.parse.com', 443)
#     params = urllib.urlencode({"where":json.dumps({
#        "currentLocation": {
#          "$nearSphere": {
#            "__type": "GeoPoint",
#            "latitude": latitude,
#            "longitude": longitude
#          },
#          "$maxDistanceInMiles": radius
#        },
#        "channels" : channel
#      })})
#     connection.connect()
#     connection.request('GET', '/1/classes/User?%s' % params, '', {
#        "X-Parse-Application-Id": "zvIWkpNTutTz3MFfP4sa7WpzjoJ4bbxjRbc62FiW",
#        "X-Parse-REST-API-Key": "5vaJiWwBd46tQaXQbBs75WHek4TrIONo6SWoYrhX"
#      })
#     result = json.loads(connection.getresponse().read())
#     print result

