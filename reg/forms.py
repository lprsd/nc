from reg.models import Team
from django.forms import ModelForm
from nutils.widgets import ReadOnlyWidget
from nutils.debug import ipython

class TeamForm(ModelForm):
    class Meta:
        model = Team
        #exclude = ('ip','modified','modified_user')
        