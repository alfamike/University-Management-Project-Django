from django import forms

from registration_app.services_fabric.services_course import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'name', 'description', 'start_date', 'end_date']

    # title = forms.ModelChoiceField(
    #     queryset=services_title.get_all_titles_queryset(),
    #     widget=forms.Select(attrs={'class': 'form-control'}),
    #     empty_label="Select a Title"
    # )

    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        # Check if end_date is after start_date
        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError("End date must be after start date.")

        return cleaned_data
