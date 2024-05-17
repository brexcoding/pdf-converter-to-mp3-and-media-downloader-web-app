
from django.urls import path , include ,re_path
from django.contrib import admin
from .views import home  ,image_to_text , image_to_audio ,dow



urlpatterns = [
    
    path('' , home  ,name='home' ),
    path('image-to-text' , image_to_text) ,
    path('image-to-audio' , image_to_audio  ) ,
    path('download' , dow)
 
]