from django import forms
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory
from brainstorm.models import Idea
from anthill.projects.models import Project, Link, Role

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['slug', 'name', 'description', 'tags', 'idea']

    idea = forms.ModelChoiceField(required=False, queryset=Idea.objects.all(),
                                  widget=forms.widgets.HiddenInput())

class FeedForm(forms.Form):
    id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    title = forms.CharField(widget=forms.widgets.TextInput(attrs={'class':'title'}))
    url = forms.URLField(widget=forms.widgets.TextInput(attrs={'class':'url'}))
FeedFormSet = formset_factory(FeedForm, can_delete=True, extra=1)

def formfield_class_callback(field):
    ff = field.formfield()
    if ff:
        ff.widget.attrs['class'] = field.name
    return ff
LinkFormSet = inlineformset_factory(Project, Link, extra=3,
                                    formfield_callback=formfield_class_callback)
RoleFormSet = inlineformset_factory(Project, Role, extra=0, fields=['status'],
                                    can_delete=False,
                                    formfield_callback=formfield_class_callback)

class JoinProjectForm(forms.Form):
    message = forms.CharField(widget=forms.widgets.Textarea)

