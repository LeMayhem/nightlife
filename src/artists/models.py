import datetime
from django.conf import settings
from django.db import models
from django.forms import ValidationError
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db.models import Count

from comments.models import Comment
from nightlife.methods import PathAndRename
from tags.models import Tag

# Create your models here.
class Artist(models.Model):
    path_and_rename = PathAndRename("artists/")
    
    name = models.CharField(max_length=255, unique=True, verbose_name="Nom de l'artiste")
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    created_on = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False, verbose_name="Publié")
    is_sponsored = models.BooleanField(default=False, verbose_name="Sponsorisé")
    biography = models.TextField(blank=True, verbose_name="Biographie")
    thumbnail = models.ImageField(blank=True, upload_to=path_and_rename)
    spotify = models.CharField(max_length=255, blank=True)
    soundcloud = models.URLField(max_length=255, blank=True)
    instagram = models.URLField(max_length=255, blank=True)
    facebook = models.URLField(max_length=255, blank=True)
    playlist = models.CharField(max_length=255, blank=True)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="fan")
    tags = models.ManyToManyField(Tag, related_name='artist_tags')
    comments = models.ManyToManyField(Comment, related_name='artist_comments', blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Artiste"

    def __str__(self):
        return self.name
    
    def clean(self):
        #Lancer le contrôle de la présence de l'artiste que sur le create
        if not self.pk:
            if Artist.objects.filter(name=self.name).exists():
                raise ValidationError({'name': _('L\'artiste existe déjà.')})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        return super().save(*args, **kwargs)
    
    #Définir la redirection
    def get_absolute_url(self):
        return reverse("artists:artist", kwargs={"slug": self.slug})
    
    def total_followers(self):
        return self.followers.count()
    
    def get_artists_with_common_tags(self):
        return Artist.objects.filter(tags__in=self.tags.all()) \
            .exclude(id=self.id) \
            .annotate(num_common_tags=Count('tags')) \
            .order_by('-num_common_tags')[:5]