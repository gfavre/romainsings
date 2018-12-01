# -*- coding: utf-8 -*-
from rest_framework import viewsets

from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .forms import SongUploadForm
from .models import Song
from .serializers import SongSerializer


class SongViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

    # todo: recherche par qr


class SongUploadView(CreateView):
    form_class = SongUploadForm
    template_name = 'songs/song_upload.html'
    success_url = reverse_lazy('songs:upload')


class AllSongsView(ListView):
    queryset = Song.objects.order_by('-created')
    template_name = "songs/songs.html"
    context_object_name = 'songs'
