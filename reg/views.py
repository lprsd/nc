# Create your views here.

import ho.pisa as pisa

from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string

from nutils.debug import *

from reg.models import Team
from reg.forms import TeamForm
import StringIO

def register(request):
    if request.method == 'POST':
        return redirect('http://nikecup.in')
    return render_to_response('register.html',
                              {},
                              RequestContext(request))

def registered(request,pk,asstring=False):
    team = get_object_or_404(Team,pk=pk)
    #form = TeamForm(instance=team)
    func = render_to_string if asstring else render_to_response
    return func('registered.html',
                locals(),
                RequestContext(request))

def download(request,pk):
    pdf_html = registered(request,pk,asstring=True)
    myfile = StringIO.StringIO()
    pisa.CreatePDF(pdf_html, myfile)
    myfile.seek(0)
    response =  HttpResponse(myfile, mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=nikecup.pdf'
    return response


def email_pdf(request):
    
    return HttpResponse('yay')
    