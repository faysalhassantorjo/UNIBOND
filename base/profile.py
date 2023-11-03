from django.forms import ModelForm
from .models import Room,UserProfile
class Profile(ModelForm):
    class Meta:
        model=UserProfile
        fields= '__all__'
        exclude=['host','participants']