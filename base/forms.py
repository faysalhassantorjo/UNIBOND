from django.forms import ModelForm
from .models import Room,UserProfile

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude=['host','participants']


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['status', 'currently_studying', 'companyName', 'current_job', 'phon_number', 'image']
