from django import forms
from .models import Message

class UserImageForm(forms.ModelForm):
    class Meta:
        model=Message
        fields=['image']