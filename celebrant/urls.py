from django.http import HttpResponse
from django.urls import path
from . import views


app_name = 'birthday_app'

urlpatterns = [
     path('', lambda request: HttpResponse("🎉 Jamani is Live!")),
    #path('', views.home_page, name='home'),
    path('upload-video/', views.upload_video, name='upload_video'),
    path('video-gallery/', views.video_gallery, name='video_gallery'),
    path('rsvp/', views.rsvp_view, name='rsvp'),
    path('rsvp/success/<int:rsvp_id>/', views.rsvp_success, name='rsvp_success'),
    ]
