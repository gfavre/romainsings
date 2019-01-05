from collections import OrderedDict
from datetime import timedelta

from django.db.models import Count, DateField
from django.views.generic import TemplateView
from django.db.models.functions import Trunc


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
        context['total_songs'] = Song.objects.count()
        plays_per_day = PlayedEvent.objects.annotate(date=Trunc('created', 'day', output_field=DateField()))\
                                           .values('date')\
                                           .annotate(plays=Count('id'))\
                                           .order_by('date')
        plays_per_day_dict = OrderedDict((ppd['date'], ppd['plays']) for ppd in plays_per_day)
        min_date = next(iter(plays_per_day_dict))
        max_date = next(reversed(plays_per_day_dict))
        context['play_per_day_labels'] = [min_date] + [min_date + timedelta(days=i) for i
                                                       in range(0, (max_date-min_date).days)]
        context['play_per_day_values'] = [plays_per_day_dict.get(thedate, 0) for thedate
                                          in context['play_per_day_labels']]
        return context
