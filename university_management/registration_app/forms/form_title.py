from django import forms

from registration_app.models import Title


class TitleForm(forms.ModelForm):
    class Meta:
        model = Title
        fields = ['name', 'description']
