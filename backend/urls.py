from django.urls import path

from backend.views import *

urlpatterns = [
    path('download/', download_yt_url, name='download_yt_url')
]
