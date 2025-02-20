import datetime
from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaultfilters import slugify
from django.views.generic.edit import ModelFormMixin
from django.db.models import Count

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from accounts.models import CustomUser
from artists.models import Artist
from events.models import Event
from blog.models import BlogPost

class Home(ListView):
    model = Event
    context_object_name = "events"
    template_name = "events/home.html"

    def get_queryset(self):
        current_week = datetime.date.today().isocalendar()[1] 
        queryset = {'featured_articles': BlogPost.objects.filter(is_featured = True).order_by('-created_on')[:4],
                    'best_events_of_the_week': Event.objects.filter(starts__week=current_week, published = True).annotate(interested_count=Count('interested')).order_by('-interested_count')[:4],
                    'favourite_artists': Artist.objects.annotate(followers_count=Count('followers')).order_by('-followers_count')[:4],
                    'last_events': Event.objects.filter(published = True).order_by('-created_on')[:4],
                    'top_promoters': CustomUser.objects.annotate(events_count=Count('promoter')).order_by('-events_count')[:4]}

        return queryset


class EventsList(ListView):
    model = Event
    context_object_name = "events"
    template_name = "events/event_list.html"

    def get_queryset(self):
        queryset = {'current_events': Event.objects.filter(starts__date__gte=datetime.datetime.now(), published=True).order_by('starts'),
                    'past_events': Event.objects.filter(starts__date__lt=datetime.datetime.now(), published=True).order_by('-starts')}

        return queryset
    
@method_decorator(login_required, name="dispatch")
class EventCreate(CreateView):
    model = Event
    template_name = "events/event_create.html"
    fields = ['title', 'starts', 'ends', 'location', 'address', 'content', 'thumbnail', 'price', 'tags', 'artists']

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.promoter = self.request.user
        
        form.instance.created_on = datetime.datetime.now()
        
        return super().form_valid(form)
    

@method_decorator(login_required, name="dispatch")
class EventUpdate(UpdateView):
    model = Event
    template_name = "events/event_update.html"
    fields = ['title', 'starts', 'ends', 'location', 'address', 'content', 'thumbnail', 'price', 'tags',  'artists', 'published']

class EventDetail(DetailView):
    model = Event
    template_name = "events/event_detail.html"
    context_object_name = "event"

@method_decorator(login_required, name="dispatch")
class EventDelete(DeleteView):
    model = Event
    context_object_name = "event"
    success_url = reverse_lazy("events:list")

@login_required
def EventInterestedView(request, slug):
    context = {}
    event = get_object_or_404(Event, slug=slug)
    if event.interested.filter(id=request.user.id).exists():
        event.interested.remove(request.user)
    else:
        event.interested.add(request.user)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def Search(request):
    if request.method == 'POST':
        search_query = request.POST['search_query']
        events = Event.objects.filter(title__unaccent__icontains=search_query)
        artists = Artist.objects.filter(name__unaccent__icontains=search_query)
        blogposts = BlogPost.objects.filter(title__unaccent__icontains=search_query)
        return render(request, "events/search_results.html", {'search_query': search_query, 'events': events, 'artists': artists, 'blogposts': blogposts})
    else:
        return render(request, "events/search_results.html")
