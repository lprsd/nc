from django.db import models
from django.contrib.auth.models import User

# Create your models here.

stores = (('LP', 'Lower Parel'),
          ('LR', 'Linking Road'),
          ('MU', 'Mulund (W)'),
          ('WO', 'Worli'))

class Team(models.Model):
    name = models.CharField(max_length=127)
    address = models.CharField(max_length=127)
    address2 = models.CharField(max_length=127)
    phone = models.CharField(max_length=127)
    email = models.EmailField(max_length=127)
    store = models.CharField(choices=stores,max_length=10)
    captain_name = models.CharField(max_length=127)
    
    nregnum = models.IntegerField(verbose_name="Nikecup Reg. No.")
    
    # Meta Fields
    datetime = models.DateTimeField(auto_now_add=True)
    ip = models.IPAddressField(null=True,blank=True)
    
    modified = models.DateTimeField(auto_now=True)
    modified_user = models.ForeignKey(User,null=True,blank=True)
    
    def send_pdf(self):
        pass
    
    def __unicode__(self):
        return self.name
    
    def save(self,*args,**kwargs):
        if not self.pk:
            self.nregnum = self.pk
        super(self,Team).save(*args,**kwargs)
    
class Player(models.Model):
    team = models.ForeignKey(Team)