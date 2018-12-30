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
    template_name = "songs/songs_list.html"
    context_object_name = 'songs'


class CardsSongsView(ListView):
    template_name = "songs/songs.html"
    context_object_name = 'songs'

    def get_queryset(self):
        qs = Song.objects.all()
        if 's' in self.request.GET:
            songs = self.request.GET.getlist('s')
            qs = qs.filter(uuid__in=songs)
        if 'of' in self.request.GET:
            order_field = self.request.GET['of']
            if order_field in [field.name for field in Song._meta.get_fields()]:
                order_direction = self.request.GET.get('od', 'asc')
                if order_direction == 'desc':
                    qs = qs.order_by('-' + order_field)
                else:
                    qs = qs.order_by(order_field)
        else:
            qs = qs.order_by('-created')

        return qs
