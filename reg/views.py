# Create your views here.

import ho.pisa as pisa

from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from nutils.debug import *

from reg.models import Team, PdfDownload
#from reg.forms import TeamForm
import StringIO
WorkingKey = 'rj2wyllcokw0svvv1f'

def register(request):
    if request.method == 'POST':
        ipython()
        pd = request.POST
        team = Team()
        team.name = pd['TeamName']
        team.address = pd['address']
        team.address2 = pd['address2']
        team.phone = pd['Phone']
        team.email = pd['email']
        team.captain_name = pd['captain']
        team.store = pd['NikeStore']
        team.ip = request.META['REMOTE_ADDR']
        team.save()
        #team.email_pdf()
        team.email_attach_pdf()
        return redirect('http://nikecup.in/index2.html')
        #return redirect(download,pk=team.pk)
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


def page2(request,pk):
    team = get_object_or_404(Team,pk=pk)
    file_name = team.merge_pages()
    only_file_name = file_name.split('/')[-1]
    return redirect('/media/finalpdfs/%s'%only_file_name)
    
def download_pdf_hash(request,team_hash):
    team = get_object_or_404(Team,nregnum=team_hash)
    file_name = team.merge_pages()
    only_file_name = file_name.split('/')[-1]
    return redirect('/media/finalpdfs/%s'%only_file_name)
    

def teams_redirect(request):
    return redirect('/admin/reg/team/')

def downloads_redirect(request):
    return redirect('/admin/reg/pdfdownload/')


def download_slno_only(request):
    pd = PdfDownload()
    pd.ip_address = request.META['REMOTE_ADDR']
    pd.save()
    return redirect(pd.get_dl_url())

def paymentpk(request,pk):
    team = get_object_or_404(Team,pk=pk)
    return payment(request,team.nregnum)


def payment(request,team_hash,payload_only=False):
    team = get_object_or_404(Team, nregnum=team_hash)
    from zlib import adler32
    params = { 'Order_Id' : team_hash,
               'Amount' : 5,
               'Merchant_Id' : 'M_Wizcraft_12245',
               'billing_cust_country' : 'India',
               'billing_cust_tel' : team.phone,
               'billing_cust_email' : team.email,
               'Redirect_Url': 'http://smackaho.st/payment-done/',
               }
    adler_string = "%s|%s|%s|%s|%s"%(params['Merchant_Id'],
                                     params['Order_Id'],
                                     params['Amount'],
                                     params['Redirect_Url'],
                                     WorkingKey)
    CheckSum = adler32(adler_string)
    params['Checksum'] = CheckSum
    #billing_zip_code
    #billing_cust_state
    #billing_cust_city
    #billing_cust_notes
    #delivery_cust_name
    #delivery_cust_address
    #delivery_cust_tel
    #delivery_zip_code
    #delivery_cust_state
    #delivery_cust_city
    if payload_only:
        return locals()
    return render_to_response('payment.html',
                              {'pp':params},
                              RequestContext(request))

def verify_checksum(params):
    adler_string = "%s|%s|%s|%s|%s"%(params['Merchant_Id'],
                                     params['Order_Id'],
                                     params['Amount'],
                                     params['AuthDesc'],
                                     WorkingKey)
    cs_generated = adler32(adler_string)
    return cs_generated == params['Checksum']
    		

from reg.models import Payment

@csrf_exempt
def payment_done(request):
    p = request.POST
    team_hash = p['Order_Id']

    p_model = Payment()
    p_model.team = get_object_or_404(Team,nregnum=team_hash)
    storing_string = ''
    for k,v in p.items():
        storing_string= "%s : %v \n%s"%(k,v,storing_string)
    p_model.gateway_formatted_values = storing_string
    
    p_model.gateway_ordernum = team_hash
    p_model.response = p['AuthDesc']
    p_model.gateway_notes = p['Notes']
    
    p_model.gateway_amount = p['Amount']
    p_model.nbbid = p['nb_bid']
    p_model.gateway_checksum = p['Checksum']
    
    p_model.datetime = datetime.now()
    
    p_model.save()
        
    is_success = p['AuthDesc'] == 'Y'
    if is_success:
        return redirect('/payment-thanks/')
    else:
        return redirect('/payment-failure/')
    
    
    
    
