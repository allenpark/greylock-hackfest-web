from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

def wave_admin(request):
    return render_to_response("admin.html", {}, RequestContext(request))

def index(request):
    values = {}
    values['name'] = "Will Jamieson"
    values['num_users'] = 10
    return render_to_response("index.html", values, RequestContext(request))
