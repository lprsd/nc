from reg.models import Team, stores
from django import forms
from nutils.widgets import ReadOnlyWidget
from nutils.debug import ipython

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        #exclude = ('ip','modified','modified_user')
        
class NewTeamForm(forms.Form):
    TeamName = forms.CharField(max_length=50, label='Team Name')
    captain = forms.CharField(max_length=50, label="Team Captain", help_text="Captain will be the main contact")
    address = forms.CharField(max_length=50, label='Address')
    address2 = forms.CharField(max_length=50, label='', required=False)
    city = forms.CharField()
    pincode = forms.IntegerField()
    Phone = forms.IntegerField(label='Phone Number', help_text='Enter 10 digit mobile number without spaces')
    email = forms.EmailField()
    NikeStore = forms.ChoiceField(choices=stores,widget=forms.RadioSelect,label='Preferred location', help_text='In the event of your team being selected, please select preferred location to collect team docket (select ONE only):')
    
    def clean_pincode(self):
        p = self.cleaned_data['pincode']
        min_value=100000
        max_value=999999
        if min_value < p < max_value:
            return p
        raise forms.ValidationError('This Pincode is invalid')
        
    def clean_phone(self):
        min_value=8000000000
        max_value=9999999999
        if min_value < p < max_value:
            return p
        raise forms.ValidationError('This is not a valid mobile phone number')
    
    def clean_email(self):
        e = self.cleaned_data['email']
        email_num = Team.objects.filter(email=e).count()
        if email_num:
            raise forms.ValidationError('This email is already registered for the Nikecup. Please check the email for the Reg form.')
        return e
    
    def save(self,**kwargs):
        pd = self.cleaned_data
        team = Team()
        team.name = pd['TeamName']
        team.address = pd['address']
        team.address2 = pd['address2']
        team.phone = pd['Phone']
        team.email = pd['email']
        team.captain_name = pd['captain']
        team.store = pd['NikeStore']
        team.save(**kwargs)
        return team
    
    