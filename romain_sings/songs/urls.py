# -*- coding: utf-8 -*-
from django.urls import path

from rest_framework import routers

from .views import SongViewSet, SongUploadView, AllSongsView


router = routers.DefaultRouter()
router.register(r'songs', SongViewSet)

app_name = "songs"

urlpatterns = [
    path("", view=AllSongsView.as_view(), name="list"),
    path("upload/", view=SongUploadView.as_view(), name="upload"),

    # path("<uuid:song>/", view=SongDetailView.as_view(), name="detail"),
]
