from django.shortcuts import render,redirect
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import  UserCreationForm
from .imageForm import UserImageForm
from django.shortcuts import get_object_or_404
# Create your views here.
from  .forms import RoomForm
# from .profile import Profile

from .models import Room,Topic,Message,UserProfile

from django.db.models import Q


def addTopic(request):
    if request.method=='POST':
        activity=request.POST.get("activity")
        obj=Topic.objects.create(name=activity)
        obj.save()
        print(activity)
        return redirect('home')
    return render(request,'base/topic_create.html')

def userProfile(request,pk):
    user=User.objects.get(id=pk)
    userinfo,created=UserProfile.objects.get_or_create(user=user)
    rooms=user.room_set.all() # eknae user object er joto gula room(Model) ace sob peye jabo
    room_messages=user.message_set.all()
    topics=Topic.objects.all()
    context={'user':user,'room_messages':room_messages,'topics':topics,'userInfo':userinfo}
    print(f'{user} userinfo: ',userinfo.currently_studying)
  
    context={
        'phon_number':userinfo.phon_number,
        'current_job':userinfo.current_job,
        'currently_studying':userinfo.currently_studying,
        'companyName':userinfo.companyName,
        'status':userinfo.status,
        'image':userinfo.imageURL,
        'rooms':rooms,
        'room_creator':user,
        'room_creator_mail':user.email,
        'id':pk
    }
    return render(request,'base/profile.html',context)
from django.urls import reverse
from .forms import UserProfileForm
def updateProfile(request,pk):
    user_profile = get_object_or_404(UserProfile, user__id=pk)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=pk)
    else:
        form = UserProfileForm(instance=user_profile)

    context = {
        'form': form,
        'id': pk,
    }
    return render(request, 'base/updateUserProfile.html', context)


def loginPage(request):

    page='login'

    if request.method=='POST':
        username=request.POST.get("username").lower()
        password=request.POST.get("password")

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,'User does not exist')

        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'username and password does not exist')

    context={'page':page}
    return render(request,'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    page='register'
    form=UserCreationForm()

    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Ann error occured during registration')

    context={'page':page,'form':form}
    return render(request,'base/login_register.html',context)

def home(request):
    q=request.GET.get('q') if request.GET.get('q') !=None else ''
    rooms=Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q)|
        Q(description__icontains=q)|
        Q(host__username__icontains=q)
    )
    # rooms=Room.objects.all()
    room_count=rooms.count()
    topics=Topic.objects.all()
    room_messages=Message.objects.filter(Q(room__name__icontains=q))

    room_participants_counts = {room.id:room.participants.count() for room in rooms}

    print('hello ', room_participants_counts)

    context = {'rooms': rooms,
               'topics':topics,
               'room_count':room_count,
               "room_messages":room_messages,
               'room_participants_counts':room_participants_counts,
                'userImage':"https://bootdey.com/img/Content/avatar/avatar7.png",
               
               }
    return render(request,"base/home.html",context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()

    

    participants = room.participants.all()
    
    number_of_participant=len(participants)

    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {
        'room': room,
        'room_messages': room_messages,
        'participants': participants,
        'number_of_participant':number_of_participant
    }
    return render(request, "base/room.html", context)
@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method=="POST":
        form=RoomForm(request.POST,request.FILES)
        if form.is_valid():
            room = form.save(commit=False)
            print(room.name)
            print(room.image)
            print(room.imageURL)
            room.host=request.user
            room.save()
        return redirect('home')
    context={"form":form}
    return render(request,'base/room_form.html',context)
from django.http import HttpResponseForbidden
@login_required(login_url='login')
def updateRoom(request, pk):
    room = get_object_or_404(Room, id=pk)

    # Check if the user is the host of the room
    if request.user != room.host:
        return HttpResponseForbidden("You are not the room creator")

    if request.method == "POST":
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            room = form.save(commit=False)
            room.save()
            return redirect('home')
    else:
        form = RoomForm(instance=room)

    context = {"form": form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})

@login_required(login_url='login')
def delete_message(request,pk):
    message=Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("your are not allowed here!!")

    if request.method=='POST':
        message.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':message})



