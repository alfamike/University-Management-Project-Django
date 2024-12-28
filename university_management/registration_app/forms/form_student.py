from django import forms
from django.core.exceptions import ValidationError

from registration_app.services_fabric.services_student import Student


class StudentForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Custom email validation: check if email ends with '@example.com'
        if not email.endswith('@example.com'):
            raise ValidationError("Email must be from the domain 'example.com'.")

        return email
