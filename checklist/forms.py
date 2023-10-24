from django import forms
from django.contrib.auth.forms import AuthenticationForm


from .models import *


class TaskSearcher(forms.ModelForm):
    search_area = models.CharField(max_length=200)

    class Meta:
        model = SetTask
        fields = '__all__'


class TaskForm(forms.ModelForm):
    
    class Meta:
        model = SetTask
        fields = ['title', 'description', 'complete']