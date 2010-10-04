from django.contrib import admin
from reg.models import Team, Player, PdfDownload, Payment
from reg.forms import TeamForm


class PdfDownloadsAdmin(admin.ModelAdmin):
    list_display = ('phash','ip_address','datetime')
    date_hierarchy = 'datetime'
    search_fields = ('phash','ip_address')
    readonly_fields = ('phash','ip_address','datetime')
    
admin.site.register(PdfDownload,PdfDownloadsAdmin)
admin.site.register(Payment)

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'nregnum', 'email', 'phone', 'store')
    date_hierarchy = 'datetime'
    search_fields = ('nregnum','name','phone','email')
    readonly_fields = ('datetime','ip','modified','modified_user','nregnum')
    fieldsets = (
        (None, {
            'fields': ('name', 'nregnum', 'captain_name')
        }),
        ('Contact details', {
            'fields': (('address','address2'),'phone','email')
        }),
        ('Meta Details', {
            'classes': ('collapse',),
            'fields': ('ip','datetime','modified','modified_user')
        }),
    )
    
    #filter_horizontal = ('store',)
    
admin.site.register(Team,TeamAdmin)
