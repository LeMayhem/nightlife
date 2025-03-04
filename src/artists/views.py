from django.utils import timezone
from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaultfilters import slugify
from django.core.files.base import ContentFile

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import requests

from artists.forms import ArtistCreateForm
from artists.models import Artist
from events.models import Event, Tag
from nightlife.spotify_methods import get_tokens, spotify_get_related_artists, spotify_search, get_authorization_url, is_user_connected, user_get_followed_artists
    
# Variables globales pour stocker l'adresse avant redirection
REFERER = None

# Ajoutez cette vue pour gérer le callback
@login_required
def spotify_callback(request):
    global REFERER
    code = request.GET.get('code')

    if code:
        access_token, refresh_token = get_tokens(code)
        if access_token:
            # Stockez les jetons dans la session ou la base de données
            request.session['access_token'] = access_token
            request.session['refresh_token'] = refresh_token
            return HttpResponseRedirect(REFERER)
        
    return render(request, 'artists/error.html', {'message': 'Erreur lors de l\'authentification avec Spotify.'})
    
@login_required
def ArtistCreate(request):
    if request.method == "POST":
        form = ArtistCreateForm(request.POST)
        if form.is_valid():
            if not is_user_connected():
                print("L'utilisateur n'est pas connecté. Redirection vers l'URL d'autorisation.")
                return redirect(get_authorization_url())
            else:
                print("L'utilisateur est déjà connecté.")

                artist = form.cleaned_data.get('name')
                artist_search = spotify_search("artist", artist)
                playlist_search = spotify_search("playlist", artist)

                new_artist = form.save(commit=False)
                new_artist.biography = form.cleaned_data.get('biography')
                new_artist.name = artist_search["name"]
                new_artist.slug = slugify(new_artist.name)
                new_artist.spotify = artist_search["id"]
                new_artist.created_on = timezone.now()
                if playlist_search:
                    new_artist.playlist = playlist_search["id"]
                    
                image_url = artist_search["images"][0]["url"]
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    image_content = ContentFile(image_response.content)
                    new_artist.thumbnail.save(f"{new_artist.name}.jpg", image_content)

                new_artist.save()

                for genre in artist_search["genres"]:
                    tag = Tag.objects.filter(slug=slugify(genre)).first()
                    if not tag:
                        tag = Tag(
                            name = genre,
                            slug=slugify(genre)
                        )
                        tag.save()
                    new_artist.tags.add(tag)

                return redirect('artists:artist', new_artist.slug)
    else:
        form = ArtistCreateForm()

    return render(request, "artists/artist_create.html", {"form": form})

@login_required
def ArtistCreateSpotifyFollowings(request):
    if not is_user_connected():
        print("L'utilisateur n'est pas connecté. Redirection vers l'URL d'autorisation.")
        global REFERER
        REFERER = request.META.get("HTTP_REFERER")
        return redirect(get_authorization_url())
    else:
        print("L'utilisateur est déjà connecté.")
        followed_artists = user_get_followed_artists()
        if followed_artists is None:
            return render(request, 'artists/error.html', {'message': 'Erreur lors de la récupération des artistes suivis.'})
        
        artists = []
        for followed_artist in followed_artists:
            if not Artist.objects.filter(slug=slugify(followed_artist['name'])).exists():
                playlist_search = spotify_search("playlist", followed_artist['name'])
                playlist = playlist_search["id"] if playlist_search else ""
                image_url = followed_artist['images'][0]['url'] if followed_artist['images'] else None
                image_content = None
                if image_url:
                    image_response = requests.get(image_url)
                    if image_response.status_code == 200:
                        image_content = ContentFile(image_response.content)
                
                artist = Artist(
                    name=followed_artist['name'],
                    slug=slugify(followed_artist['name']),
                    spotify=followed_artist['id'],
                    created_on=timezone.now(),
                    playlist=playlist,
                )
                if image_content:
                    artist.thumbnail.save(f"{followed_artist['name']}.jpg", image_content)
                artist.save()

                for genre in followed_artist["genres"]:
                    tag = Tag.objects.filter(slug=slugify(genre)).first()
                    if not tag:
                        tag = Tag(
                            name = genre,
                            slug=slugify(genre)
                        )
                        tag.save()
                    artist.tags.add(tag)

                artists.append(artist)
        return render(request, "artists/artists_list_import_confirmed.html", {"artists": artists})
    

@login_required
def ArtistFollowSpotifyFollowings(request):
    if not is_user_connected():
        print("L'utilisateur n'est pas connecté. Redirection vers l'URL d'autorisation.")
        global REFERER
        REFERER = request.META.get("HTTP_REFERER")
        return redirect(get_authorization_url())
    else:
        print("L'utilisateur est déjà connecté.")
        followed_artists = user_get_followed_artists()
        if followed_artists is None:
            return render(request, 'artists/error.html', {'message': 'Erreur lors de la récupération des artistes suivis.'})
        
        for followed_artist in followed_artists:
            if Artist.objects.filter(slug=slugify(followed_artist['name'])).exists():
                artist = get_object_or_404(Artist, slug=slugify(followed_artist['name']))
                if not artist.followers.filter(id=request.user.id).exists():
                    artist.followers.add(request.user)
                
        return render(request, "registration/user_followings.html")

    
@method_decorator(login_required, name="dispatch")
class ArtistCreateManual(CreateView):
    model = Artist
    template_name = "artists/artist_create.html"
    fields = ['name', 'biography','thumbnail','spotify','soundcloud','instagram','facebook', 'playlist']

    def form_valid(self, form):      
        form.instance.created_on = timezone.now(),
        return super().form_valid(form)
    
class ArtistsList(ListView):
    model = Artist
    context_object_name = "artists"
    template_name = "artists/artists_list.html"
    #paginate_by = 24

    def get_queryset(self):
        queryset = super().get_queryset().order_by('name')

        return queryset

@method_decorator(login_required, name="dispatch")
class ArtistUpdate(UpdateView):
    model = Artist
    template_name = "artists/artist_update.html"
    fields = ['name', 'biography','thumbnail','spotify','soundcloud','instagram','facebook', 'playlist']

class ArtistDetail(DetailView):
    model = Artist
    template_name = "artists/artist_detail.html"
    context_object_name = "artist"

    def get_context_data(self, **kwargs: Any) -> dict:
        context = super().get_context_data(**kwargs)
        artist = self.get_object()
        context['artists_with_common_tags'] = artist.get_artists_with_common_tags()

        return context

@method_decorator(login_required, name="dispatch")
class ArtistDelete(DeleteView):
    model = Artist
    context_object_name = "artist"
    success_url = reverse_lazy("artists:list")

@login_required
def ArtistFollowingView(request, slug):
    context = {}
    artist = get_object_or_404(Artist, slug=slug)
    if artist.followers.filter(id=request.user.id).exists():
        artist.followers.remove(request.user)
    else:
        artist.followers.add(request.user)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))