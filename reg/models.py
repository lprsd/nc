from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.

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
    
    modified = models.DateTimeField(verbose_name='Modified At')
    modified_user = models.ForeignKey(User,null=True,blank=True,verbose_name='Modified by')
    
    def send_pdf(self):
        pass
    
    def __unicode__(self):
        return self.name
    
    def save(self,*args,**kwargs):
        if not self.nregnum:
            import random
            rn = int(str(random.random())[2:10])
            self.nregnum = rn
        super(Team,self).save(*args,**kwargs)
    
class Player(models.Model):
    team = models.ForeignKey(Team)