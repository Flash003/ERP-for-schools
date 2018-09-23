from django import forms
from Darwin.models import Announcement

class create_announcement_form(forms.ModelForm):

    class Meta:
        model = Announcement
        fields = ('heading', 'content', 'date_and_time', 'author')
