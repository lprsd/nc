from django.contrib import admin
from reg.models import Team, Player, PdfDownload, Payment
from reg.forms import TeamForm
from django import forms
from form_utils.fields import ClearableImageField
from form_utils.forms import BetterModelForm
from form_utils.widgets import ImageWidget, AutoResizeTextarea, InlineAutoResizeTextarea
from django.db import models

class PdfDownloadsAdmin(admin.ModelAdmin):
    list_display = ('phash','ip_address','datetime')
    date_hierarchy = 'datetime'
    search_fields = ('phash','ip_address')
    readonly_fields = ('phash','ip_address','datetime')
    
admin.site.register(PdfDownload,PdfDownloadsAdmin)
admin.site.register(Payment)
admin.site.register(Player)

from nutils.debug import ipython

class PlayerAdminForm(forms.ModelForm):
    
    address = forms.CharField(widget=InlineAutoResizeTextarea)
    ailments = forms.CharField(required=False)
    
    class Meta:
        model = Player
        #fieldsets = (
            #(None, {'fields': ('name', 'photo')}),
            #('ABCD', {'fields': ('address', 'ailments')})
        #)
        
        
from django.contrib.admin.options import InlineModelAdmin

class PlayerInline(admin.TabularInline):
    model = Player
    form = PlayerAdminForm
    formfield_overrides = { models.ImageField: {'widget': ImageWidget}}
    template = 'stacked.html'
    #show_url = True
    fieldsets = (
            ('', {'fields': ('name', 'photo', 'dob', 'email')}),
            ('', {'fields': ('address', 'mobile_phone', 'land_phone')}),
            ('', {'fields': ('emergency_contact', 'receive_updates')})
        )
    
class PaymentInline(admin.TabularInline):
    model = Payment
    fieldsets = (
        (None, {'fields': ('name', 'photo')}),
        ('ABCD', {'fields': ('address', 'ailments')})
    )
    
    
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'datetime', 'nregnum', 'email', 'phone', 'store', 'payment_done', 'payment_detail', 'status', 'players')
    date_hierarchy = 'datetime'
    search_fields = ('nregnum','name','phone','email')
    readonly_fields = ('datetime','ip','modified','modified_user','nregnum')
    fieldsets = (
        (None, {
            'fields': ('name', 'nregnum', 'status')
        }),
        ('Contact details', {
            'classes': ('collapse',),
            'fields': ('captain_name',('address','address2'),'phone','email')
        }),
        ('Meta Details', {
            'classes': ('collapse',),
            'fields': ('ip','datetime','modified','modified_user')
        }),
    )
    inlines = [PlayerInline]
    #filter_horizontal = ('store',)
    
admin.site.register(Team,TeamAdmin)
