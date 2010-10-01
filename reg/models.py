from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.conf import settings
# Create your models here.

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

import os

pixel = 0.72 # point = 0.75* pixel
MAX_Y_POINT_A4 = 841.88


stores = (('LP', 'Lower Parel'),
          ('LR', 'Linking Road'),
          ('MU', 'Mulund (W)'),
          ('WO', 'Worli'))

page2_positions = {
    'nregnum': (59,57),
    'name': (75,215),
    'captain_name': (152,230),
    'phone': (121,245),
    'email': (347,245),
    'address': (87,261),
    'address2': (30, 275),
    }


class Team(models.Model):
    name = models.CharField(max_length=127,verbose_name='Team Name')
    address = models.CharField(max_length=127)
    address2 = models.CharField(max_length=127)
    phone = models.CharField(max_length=127)
    email = models.EmailField(max_length=127)
    store = models.CharField(choices=stores,max_length=10)
    captain_name = models.CharField(max_length=127)
    
    nregnum = models.IntegerField(verbose_name="Nikecup Reg. No.")
    
    # Meta Fields
    datetime = models.DateTimeField(verbose_name='Created At')
    ip = models.IPAddressField(null=True,blank=True,verbose_name='IP address of creator')
    
    modified = models.DateTimeField(verbose_name='Modified At',blank=True,null=True)
    modified_user = models.ForeignKey(User,null=True,blank=True,verbose_name='Modified by')
    
    def send_pdf(self):
        pass
    
    def create_page2_pdf(self):
        sign_file_name = "%spdfs/pk%s.pdf"%(settings.MEDIA_ROOT,self.id)
        file_exists = os.path.isfile(sign_file_name)
        #if file_exists:
            #os.remove(sign_file_name)
        p = canvas.Canvas(sign_file_name,pagesize=A4,bottomup=0)
        p.setFillColorRGB(0,0,0)
        FONT_SIZE = 9
        p.setFontSize(size=FONT_SIZE)
        for att_name,(x_coord,y_coord) in page2_positions.items():
            att = str(getattr(self,att_name))
            p.drawString(x_coord,y_coord+5,att)
        p.showPage()
        p.save()
        #print sign_file_name
        return sign_file_name

    def merge_pages(self):
        from pyPdf import PdfFileReader,PdfFileWriter
        
        pdf_file = "%smain.pdf"%settings.MEDIA_ROOT
        pdf_obj = PdfFileReader(open(pdf_file))
        
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
        from django.core.mail import send_mail
        from django.template.loader import render_to_string
        message = render_to_string('email.txt',{'team':self})
        send_mail(subject='Nike Cricket Registration',
                  message=message,
                  from_email='noreply@nikecricket.in',
                  recipient_list=(self.email,))
        
    def email_attach_pdf(self):
        pass
        
    def __unicode__(self):
        return self.name
    
    def save(self,*args,**kwargs):
        if not self.nregnum:
            import random
            rn = int(str(random.random())[2:10])
            self.nregnum = rn
        if not self.pk:
            self.datetime = datetime.now()
        super(Team,self).save(*args,**kwargs)
    
class Player(models.Model):
    team = models.ForeignKey(Team)