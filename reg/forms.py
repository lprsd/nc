from reg.models import Team
from django.forms import ModelForm
from nutils.widgets import ReadOnlyWidget
from nutils.debug import ipython

class TeamForm(ModelForm):
    def __init__(self,*args,**kwargs):
        #ipython()
        for el in self.base_fields.values():
            ipython()
            el.widget = ReadOnlyWidget(el.value)
        super(self,Team).__init__(*args,**kwargs)
    
    class Meta:
        model = Team
        exclude = ('ip','modified','modified_user')