from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
# Create your models here.

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

import os

pixel = 0.75 # point = 0.75* pixel
MAX_Y_POINT_A4 = 841.88


stores = (('LP', 'Nike store, Lower Parel'),
          ('LR', 'Nike store, Linking Road'),
          ('MU', 'Nike store, Mulund (W)'),
          ('WO', 'Nike store, Worli'))

page2_positions = {
    'nregnum': (59,57),
    'name': (75,215),
    'captain_name': (152,230),
    'phone': (121,245),
    'email': (347,245),
    'address': (87,261),
    'address2': (30, 275),
    }

positions_2011_dl = {
    'phash': (73,93),
    }

positions_2011 = {
    'nregnum': (73,93),
    'name': (88,235),
    'captain_name': (402,235),
    'phone': (131,253),
    'email': (349,253),
    'address': (97,270),
    'city': (60, 286),
    'pincode': (360,286)
    }

file_names = {
    'dl_raw': "%spdf_dl_raw/pk%s.pdf",
    'dl_done': '%spdf_dl/NikeCup%s.pdf',
    'entered_raw': '%spdfs/pk%s.pdf',
    'entered_done': "%sfinalpdfs/NikeCup%s.pdf",
    'main_pdf': "%srf2.pdf",
    'mum_pdf': "%smum.pdf",
    'del_pdf': "%sdel.pdf"
}

class PdfDownload(models.Model):
    phash = models.IntegerField()
    ip_address = models.IPAddressField()
    datetime = models.DateTimeField()
    
    def get_dl_url(self):
        self.merge_pdf()
        return (file_names['dl_done']%(settings.MEDIA_URL,self.phash))

    def get_url(self,file_name='mum_pdf'):
        self.merge_pdf(file_name=file_name)
        return (file_names['dl_done']%(settings.MEDIA_URL,self.phash))

    
    def make_pdf(self):
        sign_file_name = file_names['dl_raw']%(settings.MEDIA_ROOT,self.pk)
        p = canvas.Canvas(sign_file_name,pagesize=A4,bottomup=0)
        p.setFillColorRGB(0,0,0)
        FONT_SIZE = 9
        p.setFontSize(size=FONT_SIZE)
        for att_name,(x_coord,y_coord) in positions_2011_dl.items():
            att = str(getattr(self,att_name))
            p.drawString(x_coord,y_coord+20,att)
        p.showPage()
        p.save()
        #print sign_file_name
        return sign_file_name
    
    def merge_pdf(self,file_name='main_pdf'):
        from pyPdf import PdfFileReader,PdfFileWriter
                
        pdf_file = file_names[file_name]%settings.MEDIA_ROOT
        pdf_obj = PdfFileReader(open(pdf_file))
        
        values_page = PdfFileReader(open(self.make_pdf())).getPage(0)
        
        mergepage = pdf_obj.pages[0]
        mergepage.mergePage(values_page)
        
        mergepage = pdf_obj.pages[1]
        mergepage.mergePage(values_page)
        
        signed_pdf = PdfFileWriter()
        for page in pdf_obj.pages:
            signed_pdf.addPage(page)

        signed_pdf_name = file_names['dl_done']%(settings.MEDIA_ROOT,self.phash)
        signed_pdf_file = open(signed_pdf_name,mode='wb')
        
        signed_pdf.write(signed_pdf_file)
        signed_pdf_file.close()
        return signed_pdf_name

    def save(self,*args,**kwargs):
        if not self.phash:
            import random
            rn = int(str(random.random())[2:10])
            self.phash = rn
        if not self.pk:
            self.datetime = datetime.now()
        super(PdfDownload,self).save(*args,**kwargs)

status = ((0,'Pending'),
          (1,'Approved'),
          (2,'Rejected'),
          )

class Team(models.Model):
    name = models.CharField(max_length=127,verbose_name='Team Name')
    address = models.CharField(max_length=127)
    address2 = models.CharField(max_length=127,blank=True,null=True)
    city = models.CharField(max_length=50)
    pincode = models.IntegerField(default=12345)
    phone = models.CharField(max_length=127,blank=True,null=True)
    email = models.EmailField(max_length=127,blank=True,null=True)
    store = models.CharField(choices=stores,max_length=10)
    captain_name = models.CharField(max_length=127,blank=True,null=True)
    
    nregnum = models.IntegerField(verbose_name="Nikecup Reg. No.")
    
    # Meta Fields
    datetime = models.DateTimeField(verbose_name='Created At')
    ip = models.IPAddressField(null=True,blank=True,verbose_name='IP address of creator')
    
    modified = models.DateTimeField(verbose_name='Modified At',blank=True,null=True)
    modified_user = models.ForeignKey(User,null=True,blank=True,verbose_name='Modified by')
    
    payment_done = models.BooleanField(default=False)
    payment_detail = models.TextField()
    
    status = models.PositiveSmallIntegerField(choices=status,default=0)
    
    print_fields = ['name','address','address2','city','pincode','phone','email','store','captain_name']
    
    def get_print_dict(self):
        from django.utils.datastructures import SortedDict
        s = SortedDict()
        for el in self.print_fields:
            s[el] = getattr(self,el)
        return s
    
    def players(self):
        return self.player_set.count()
    
    def create_page2_pdf(self):
        sign_file_name = "%spdfs/pk%s.pdf"%(settings.MEDIA_ROOT,self.id)
        file_exists = os.path.isfile(sign_file_name)
        if file_exists:
            os.remove(sign_file_name)
            print 'Existing file removed'
        p = canvas.Canvas(sign_file_name,pagesize=A4,bottomup=0)
        p.setFillColorRGB(0,0,0)
        FONT_SIZE = 9
        p.setFontSize(size=FONT_SIZE)
        for att_name,(x_coord,y_coord) in positions_2011.items():
            att = str(getattr(self,att_name))
            p.drawString(x_coord,y_coord+8,att)
        p.showPage()
        p.save()
        #print sign_file_name
        return sign_file_name

    def merge_pages(self,pdf='mum_pdf'):
        from pyPdf import PdfFileReader,PdfFileWriter
        
        pdf_file = file_names[pdf]%settings.MEDIA_ROOT
        pdf_obj = PdfFileReader(open(pdf_file))
        
        ##This is a bug in pyPdf. It detects some files as encrypted, even if they are not. It can be circumvented by asking it to decrypt with an empty string.
        #if pdf_obj.isEncrypted:
            #pdf_obj.decrypt('')
        

        
        values_page = PdfFileReader(open(self.create_page2_pdf())).getPage(0)
        
        mergepage = pdf_obj.pages[1]
        mergepage.mergePage(values_page)
        
        signed_pdf = PdfFileWriter()
        for page in pdf_obj.pages:
            signed_pdf.addPage(page)

        signed_pdf_name = "%s/finalpdfs/NikeCup%s.pdf"%(settings.MEDIA_ROOT,self.nregnum)
        signed_pdf_file = open(signed_pdf_name,mode='wb')
        
        signed_pdf.write(signed_pdf_file)
        signed_pdf_file.close()
        return signed_pdf_name
    
    @models.permalink
    def get_pdf_url(self):
        return ['download_pdf_hash',(self.nregnum,)]
    
    def email_pdf(self):
        message = render_to_string('email.txt',{'team':self})
        send_mail(subject='Nike Cricket Registration',
                  message=message,
                  from_email='noreply@nikecricket.in',
                  recipient_list=(self.email,))
        
    def email_attach_pdf(self):
        message = render_to_string('email2.txt',{'team':self})
        email = EmailMessage(subject='Nike Cricket Registration',
                  body=message,
                  from_email='noreply@nikecricket.in',
                  to=(self.email,))
        email.attach_file(self.merge_pages())
        return email.send()
        
    def send_html_email(self):
        message = render_to_string('ack_mail.html',{'team':self})
        email = EmailMessage(subject='Nike Cricket Registration',
                             body=message,
                             from_email='noreply@nikecricket.in',
                             to=(self.email,))
        email.content_subtype = "html"  # Main content is now text/html
        email.attach_file(self.merge_pages())
        return email.send()
        
    
    def __unicode__(self):
        return self.name
    
    def print_team(self):
        print_url = reverse('print_team',args=[self.nregnum,])
        return '<a href="%s">Print</a>'%print_url
    print_team.allow_tags=True
    
    def download_excel(self):
        dexcel_url = reverse('download_excel',args=[self.nregnum,])
        return '<a href="%s">Download as Excel</a>'%dexcel_url
    download_excel.allow_tags=True
   
    #def send_approved_email(self):
        #dexcel_url = reverse('download_excel',args=[self.nregnum,])
        #return '<a href="%s">Download as Excel</a>'%dexcel_url
    #send_approved_email.allow_tags=True
    
    #def send_rejected_email(self):
        #dexcel_url = reverse('download_excel',args=[self.nregnum,])
        #return '<a href="%s">Download as Excel</a>'%dexcel_url
    #send_rejected_email.allow_tags=True
    
    def save(self,*args,**kwargs):
        if not self.nregnum:
            import random
            rn = int(str(random.random())[2:10])
            self.nregnum = rn
        if not self.pk:
            self.datetime = datetime.now()
        super(Team,self).save(*args,**kwargs)

from form_utils.fields import ClearableImageField        
from django.conf import settings

class Player(models.Model):
    team = models.ForeignKey(Team)
    
    name = models.CharField(max_length=100)
    dob = models.DateField()
    address = models.TextField()
    city = models.CharField(max_length=50)
    pincode = models.IntegerField()
    mobile_phone = models.IntegerField()
    land_phone = models.CharField(max_length=10)
    emergency_contact = models.CharField(max_length=100)
    email = models.EmailField()
    ailments = models.TextField(blank=True,null=True)
    receive_updates = models.BooleanField(default=True)
    photo = models.ImageField(blank=True,null=True,upload_to='photo')
    
    
#class TeamOrder(models.Model):
    #orderid = models.CharField(max_length=32)
    
    #datetime = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return "%s : %s" %(self.team.name,self.name)
    
class Payment(models.Model):
    team = models.ForeignKey(Team,null=True,blank=True)
    pdf_download = models.ForeignKey(PdfDownload,null=True,blank=True)
    order_id = models.CharField(max_length=20)

    gateway_ordernum = models.CharField(max_length=100)
    gateway_response = models.CharField(max_length='10')
    gateway_notes = models.TextField(blank=True,null=True)

    gateway_amount = models.DecimalField(decimal_places=2,max_digits=8)
    gateway_nbbid = models.CharField(max_length=32)
    gateway_formatted_values = models.TextField()
    
    gateway_checksum = models.CharField(max_length=20)
    datetime = models.DateTimeField()

    def __unicode__(self):
        return "%s" %self.team