from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

def wave_admin(request):
	return render_to_response("admin.html", {}, RequestContext(request))