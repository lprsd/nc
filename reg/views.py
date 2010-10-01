# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from nutils.debug import *

def register(request):
    if request.method == 'POST':
        return redirect('http://nikecup.in')
    return render_to_response('register.html',{},RequestContext(request))
