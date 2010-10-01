# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from nutils.debug import *

def register(request):
    if request.method == 'POST':
        ipython()
    return HttpResponse('Yay')
