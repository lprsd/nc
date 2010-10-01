from django.db import models

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
    
class Player(models.Model):
    team = models.ForeignKey(Team)