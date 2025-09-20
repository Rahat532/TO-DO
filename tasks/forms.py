from django import forms
from django.utils import timezone
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'due_date', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'What needs to be done?', 'autofocus': 'autofocus', 'class': 'border rounded-lg px-3 py-2'}),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'border rounded-lg px-3 py-2'}),
            'priority': forms.Select(attrs={'class': 'border rounded-lg px-3 py-2'}),
        }

    def clean_title(self):
        title = (self.cleaned_data.get('title') or '').strip()
        if not title:
            raise forms.ValidationError('Please enter a task title.')
        return title

    def clean_due_date(self):
        due = self.cleaned_data.get('due_date')
        if due and due < timezone.now():
            raise forms.ValidationError('Due date cannot be in the past.')
        return due
