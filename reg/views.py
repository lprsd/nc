# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from nutils.debug import *
from zlib import adler32
import time
from django.conf import settings

from reg.models import Team, PdfDownload
from reg.forms import TeamForm, NewTeamForm, Team2011Form, Team2011Form2
import StringIO
WorkingKey = 'rj2wyllcokw0svvv1f'
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

def register(request):
    form  = NewTeamForm(request.POST or None)
    if form.is_valid():
        team = form.save()
        team.ip = request.META['REMOTE_ADDR']
        team.save()
        team.send_html_email()
        return redirect(payment,team.nregnum)
        #return redirect(download,pk=team.pk)
    return render_to_response('register_form.html',
                              {'form':form},
                              RequestContext(request))

@csrf_exempt
def register2(request,template_name='index_2011.html'):
    new_post = None
    if request.method=='POST' and request.POST['city'] == 'Delhi':
        new_post = request.POST.copy()
        print 'Modified POST data'
        new_post[u'Location'] = request.POST.getlist('Location')[0]
    form  = Team2011Form(data=new_post or request.POST or None)
    if form.is_valid():
        print form.cleaned_data
        team = form.save()
        team.ip = request.META['REMOTE_ADDR']
        team.save()
        pdf_file = 'del_pdf' if team.city == 'Delhi' else 'mum_pdf'
        team.send_html_email(pdf_file=pdf_file)
        return redirect('http://www.nikecup.in/2011/standalone/registration/register-thankyou.html')
        #return redirect(download,pk=team.pk)
    return render_to_response(template_name,
                              {'form':form},
                              RequestContext(request))

def handle_uploaded_file(f):
    destination = open('/tmp/aaa/', 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

@csrf_exempt
def register3(request,template_name='index_20112.html'):
    if request.method == 'POST':
        form = Team2011Form2(request.POST,request.FILES)
        from IPython import embed
        embed()
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return redirect('http://www.nikecup.in/2011/standalone/registration/register-thankyou.html')
        #return redirect(download,pk=team.pk)
    else:
        form = Team2011Form2()
    return render_to_response(template_name,
                              {'form':form},
                              RequestContext(request))




def register_simple_2011(request):
    return register2(request,template_name='test_reg_2011.html')
    

def registered(request,pk,asstring=False):
    team = get_object_or_404(Team,pk=pk)
    #form = TeamForm(instance=team)
    func = render_to_string if asstring else render_to_response
    return func('registered.html',
                locals(),
                RequestContext(request))

#def download(request,pk):
    #pdf_html = registered(request,pk,asstring=True)
    #myfile = StringIO.StringIO()
    #pisa.CreatePDF(pdf_html, myfile)
    #myfile.seek(0)
    #response =  HttpResponse(myfile, mimetype='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename=nikecup.pdf'
    #return response


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

def download_city(request,file_name):
    pd = PdfDownload()
    pd.ip_address = request.META['REMOTE_ADDR']
    pd.save()
    return redirect(pd.get_url(file_name))

def paymentpk(request,pk):
    team = get_object_or_404(Team,pk=pk)
    return payment(request,team.nregnum)

def payment(request,team_hash,payload_only=False):
    team = get_object_or_404(Team, nregnum=team_hash)
    params = { 'Order_Id' : "%s:%s"%(team_hash,int(time.time())),
               'Amount' : 500,
               'Merchant_Id' : 'M_Wizcraft_12245',
               'billing_cust_country' : 'India',
               'billing_cust_tel' : team.phone,
               'billing_cust_email' : team.email,
               'Redirect_Url': settings.REDIRECT_URL,
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
    return render_to_response('make_payment.html',
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
    team_hash = p['Order_Id'].split(":")[0]
    #idebug()
    p_model = Payment()
    t = get_object_or_404(Team,nregnum=team_hash)
    p_model.team = t
    storing_string = ''
    for k,v in p.items():
        storing_string= "%s : %s \n%s"%(k,v,storing_string)
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
        t.payment_done = True
        t.payment_detail = 'Online %s'%p_model.pk
        t.save()
        return redirect('http://nikecup.in/index2.html')
    else:
        return redirect('/payment-fail/')
    

@login_required
def print_team(request,team_hash):
    team = get_object_or_404(Team,nregnum=team_hash)
    return render_to_response('print_team.html',
                              {'print_dict':team.get_print_dict()},
                              RequestContext(request))

    
def download_excel(request,team_hash):
    team = get_object_or_404(Team,nregnum=team_hash)
    team_dict = team.get_print_dict()
    response = HttpResponse(mimetype='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s.xls'%team.nregnum
    import csv
    writer = csv.writer(response)
    
    for k,v in team_dict.items():
        writer.writerow([k,v])
    
    return response
    
