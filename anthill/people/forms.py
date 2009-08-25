from django import forms
from anthill.people.models import ROLES
from markupfield.widgets import MarkupTextarea

DISTANCE_CHOICES = (
    ('5', '5 Miles'),
    ('25', '25 Miles'),
    ('50', '50 Miles'),
    ('100', '100 Miles'),
)

class SearchForm(forms.Form):
    location = forms.CharField(required=False)
    skills = forms.CharField(required=False)
    name = forms.CharField(required=False)
    position = forms.ChoiceField(label='Position', 
                                 choices=(('','-------'),)+ROLES,
                                 required=False)
    location_range = forms.ChoiceField(choices=DISTANCE_CHOICES, initial='50',
                                       required=False)

class ProfileForm(forms.Form):
    name = forms.CharField(label='Name', required=False)
    email = forms.CharField(label='Email')
    url = forms.URLField(label='Personal URL', required=False)
    twitter_id = forms.CharField(label='Twitter Username', max_length=15, required=False)
    position = forms.ChoiceField(label='Position', choices=ROLES)
    location = forms.CharField(label='Location', required=False)
    skills = forms.CharField(label='Skills', required=False)
    about = forms.CharField(widget=MarkupTextarea, label='About You', required=False)

class PasswordForm(forms.Form):
    password1 = forms.CharField(label='Password', 
                                widget=forms.widgets.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', 
                                widget=forms.widgets.PasswordInput)

    def clean(self):
        if self.cleaned_data.get('password1') != self.cleaned_data.get('password2'):
            raise forms.ValidationError('Passwords must match')
        return self.cleaned_data

class UserContactForm(forms.Form):
    subject = forms.CharField()
    body = forms.CharField(widget=forms.widgets.Textarea)
