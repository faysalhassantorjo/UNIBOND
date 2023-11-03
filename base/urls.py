from django.urls import path
from . import views

urlpatterns=[
  path('login/',views.loginPage,name='login'),
  path('profile/<str:pk>',views.userProfile,name='profile'),
  path('updateProfile/<str:pk>',views.updateProfile,name='updateProfile'),
  path('register/',views.registerPage,name='register'),
  path('logout/',views.logoutUser,name='logout'),
  path("",views.home,name='home'),
  path("room/<str:pk>/",views.room,name='room'),
  path("create-room/",views.createRoom,name='create_room'),
  path("update-room/<str:pk>",views.updateRoom,name='update-room'),
  path("delete-room/<str:pk>",views.deleteRoom,name='delete-room'),
  path("delete-message<str:pk>",views.delete_message,name='delete-message'),
]