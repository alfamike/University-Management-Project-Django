from django import forms

from registration_app.services_fabric.services_title import Title


class TitleForm(forms.ModelForm):
    class Meta:
        model = Title
        fields = ['name', 'description']
