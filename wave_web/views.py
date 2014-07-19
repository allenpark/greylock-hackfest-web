from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
import json, httplib, urllib

def wave_admin(request):
    values = {}
    values["channels"] = get_channels_to_review()
    return render_to_response("admin.html", values, RequestContext(request))

def index(request):
    values = {}
    values['name'] = "Will Jamieson"
    values['num_users'] = 10
    return render_to_response("index.html", values, RequestContext(request))


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
    return [(channel["objectId"], channel["name"]) for channel in result["results"]]