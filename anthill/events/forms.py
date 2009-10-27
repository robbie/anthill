import datetime
from django import forms
from anthill.events.models import Event

DISTANCE_CHOICES = (
    ('5', '5 Miles'),
    ('25', '25 Miles'),
    ('50', '50 Miles'),
    ('100', '100 Miles'),
)

class SearchForm(forms.Form):
    name = forms.CharField(required=False)
    location = forms.CharField(required=False)
    location_range = forms.ChoiceField(choices=DISTANCE_CHOICES, initial='50',
                                       required=False)

class SplitDateTimeListWidget(forms.widgets.SplitDateTimeWidget):
    def format_output(self, rendered_widgets):
        return '<li><label>Date</label>%s</li><li><label>Time</label>%s</li>' % (rendered_widgets[0],
                                                                                 rendered_widgets[1])

class SplitDateOptionalTimeField(forms.SplitDateTimeField):
    def compress(self, data_list):
        if data_list:
            # Raise a validation error if time or date is empty
            # (possible if SplitDateTimeField has required=False).
            if data_list[0] in (None, ''):
                raise ValidationError(self.error_messages['invalid_date'])
            if data_list[1] in (None, ''):
                data_list[1] = datetime.time()  # use default time
            return datetime.datetime.combine(*data_list)
        return None

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'url', 'start_date', 'end_date', 'related_projects']

    location = forms.CharField(label='Address')
    start_date = SplitDateOptionalTimeField(widget=SplitDateTimeListWidget, required=False)
    end_date = SplitDateOptionalTimeField(widget=SplitDateTimeListWidget, required=False)

class AttendForm(forms.Form):
    guests = forms.IntegerField('Additional Guests',
                                widget=forms.widgets.Select(choices=zip(range(0,10),range(0,10))))
    message = forms.CharField('Message to Event Organizer', widget=forms.widgets.Textarea)
