from django.db import models

# Create your models here.

class Team(models.Model):
    name = models.CharField(max_length=127)
    
    
    
class Player(models.Model):
    team = models.ForeignKey(Team)