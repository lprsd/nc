from reg.models import Team, stores, stores_11
from django import forms
from nutils.widgets import ReadOnlyWidget

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
    phone = forms.IntegerField(label='Phone Number', help_text='Enter 10 digit mobile number without spaces')
    email = forms.EmailField()
    NikeStore = forms.ChoiceField(choices=stores,widget=forms.RadioSelect,label='Preferred location', help_text='In the event of your team being selected, please select preferred location to collect team docket (select ONE only):')
    
    def clean_TeamName(self):
        tn = self.cleaned_data['TeamName']
        tn_count = Team.objects.filter(name=tn).count()
        if tn_count:
            raise forms.ValidationError('This Team Name is already taken. Please choose another.')
        return tn
    
    def clean_pincode(self):
        p = self.cleaned_data['pincode']
        min_value=100000
        max_value=999999
        if min_value < p < max_value:
            return p
        raise forms.ValidationError('This Pincode is invalid')
        
    def clean_phone(self):
        p = self.cleaned_data['phone']
        min_value=8000000000
        max_value=9999999999
        if not min_value < p < max_value:
            raise forms.ValidationError('This is not a valid mobile phone number')
        phone_num = Team.objects.filter(phone=p).count()
        if phone_num:
            raise forms.ValidationError('There is a nikecup team registered already, with this phone number.')
        return p

    
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
        team.phone = pd['phone']
        team.email = pd['email']
        team.captain_name = pd['captain']
        team.store = pd['NikeStore']
        team.city = pd['city']
        team.pincode = pd['pincode']
        team.save(**kwargs)
        return team
    

class Team2011Form(forms.Form):
    teamName = forms.CharField(max_length=50, label='Team Name',widget=forms.TextInput(attrs={'class':'fieldss req name','size':40}))
    teamCaptain = forms.CharField(max_length=50, label="Team Captain",widget=forms.TextInput(attrs={'class':'fieldss req name','size':40}))
    address = forms.CharField(max_length=50, label='Address',widget=forms.TextInput(attrs={'class':'fieldss req','size':40}))
    address2 = forms.CharField(max_length=50, label='', required=False,widget=forms.TextInput(attrs={'class':'fieldss','size':40}))
    city = forms.ChoiceField(choices=((None,'- Please Select -'),('Mumbai','Mumbai'),('Delhi','Delhi')),widget=forms.Select(attrs={'id':'city'}))
    pincode = forms.IntegerField(widget=forms.TextInput(attrs={'class':'fieldss','size':40}))
    phone = forms.IntegerField(label='Phone Number', widget=forms.TextInput(attrs={'class':'fieldss req name','size':40}),help_text='Enter 10 digit mobile number without spaces')
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'fieldss req name','size':40}))
    Location = forms.ChoiceField(choices=stores_11)

    def clean_TeamName(self):
        tn = self.cleaned_data['TeamName']
        tn_count = Team.objects.filter(name=tn).count()
        if tn_count:
            raise forms.ValidationError('This Team Name is already taken. Please choose another.')
        return tn
    
    def clean_pincode(self):
        p = self.cleaned_data['pincode']
        min_value=100000
        max_value=999999
        if min_value < p < max_value:
            return p
        raise forms.ValidationError('This Pincode is invalid')
        
    def clean_phone(self):
        p = self.cleaned_data['phone']
        min_value=7000000000
        max_value=9999999999
        if not min_value < p < max_value:
            raise forms.ValidationError('This is not a valid mobile phone number')
        phone_num = Team.objects.filter(phone=p).count()
        if phone_num:
            raise forms.ValidationError('There is a nikecup team registered already, with this phone number.')
        return p

    
    def clean_email(self):
        e = self.cleaned_data['email']
        email_num = Team.objects.filter(email=e).count()
        if email_num:
            raise forms.ValidationError('This email is already registered for the Nikecup. Please check the email for the Reg form.')
        return e
    
    def save(self,**kwargs):
        pd = self.cleaned_data
        team = Team()
        team.name = pd['teamName']
        team.address = pd['address']
        team.address2 = pd['address2']
        team.phone = pd['phone']
        team.email = pd['email']
        team.captain_name = pd['teamCaptain']
        team.store = pd['Location']
        team.city = pd['city']
        team.pincode = pd['pincode']
        team.save(**kwargs)
        return team
