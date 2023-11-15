from django.db import models
from django.contrib.auth.models import  User

# Create your models here.

class Topic(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return  self.name


class Room(models.Model):
    host=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    topic=models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    name=models.CharField(max_length=200)
    description=models.TextField(null=True,blank=True)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
    participants=models.ManyToManyField(User,related_name='participant',blank=True)
    image=models.ImageField(upload_to='post/',null=True,blank=True)

    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url=''
        return url

    class Meta:
        ordering=['-updated','-created']

    def __str__(self):
        return str(self.name)


class Message(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    room=models.ForeignKey(Room,on_delete=models.CASCADE)
    body=models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/',null=True, blank=True)
    
    class Meta:
        ordering=['-updated','-created']
    def __str__(self):
        return str(self.body[:50])

class UserProfile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    currently_studying=models.CharField(default=None, max_length=200,null=True)
    companyName=models.CharField(max_length=200,default=None,null=True)
    current_job=models.CharField(max_length=200,default=None,null=True)
    phon_number=models.CharField(max_length=20,default=None,null=True)
