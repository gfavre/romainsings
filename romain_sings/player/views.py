from django.db.models import Count
from django.views.generic import TemplateView

from romain_sings.songs.models import Song
from .models import PlayedEvent


class DashboardView(TemplateView):
    template_name = "pages/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_plays'] = PlayedEvent.objects.count()
        context['top5'] = PlayedEvent.objects.select_related('song')\
                                             .values('song', 'song__title')\
                                             .annotate(total_play=Count('id')).order_by('-total_play')[:5]
        return context
