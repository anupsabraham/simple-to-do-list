from django import forms
from tasks.models import Tasks


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        exclude = ('user', )