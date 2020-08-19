from django import forms
from .models import StudyModel

class SpendingForm(forms.Form):
    SUBJECT = (
    (1, 'English'),
    (2, 'Programming'),
    (3, 'Mathematics'),
    (4, 'Others')
    )
    MONTHS = {
    1:('1'), 2:('2'), 3:('3'), 4:('4'),
    5:('5'), 6:('6'), 7:('7'), 8:('8'),
    9:('9'), 10:('10'), 11:('11'), 12:('12')
    }
    date = forms.DateTimeField()
    #date = forms.DateTimeField(widget=forms.SelectDateWidget(months=MONTHS))
    subject = forms.ChoiceField(choices=SUBJECT,widget=forms.widgets.Select)
    study_time = forms.DurationField()
    content = forms.CharField(max_length=200)

class RivalForm(forms.Form):
    rival_name = forms.CharField(
        label='input rival name',
        max_length=20
    )