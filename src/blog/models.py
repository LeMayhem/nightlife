import datetime
from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

from datetime import date
import readtime
from artists.models import Artist
from events.models import Comment, Event, Tag
from nightlife.methods import PathAndRename

# Create your models here.
class BlogPost(models.Model):
    path_and_rename = PathAndRename("blog/")
    title = models.CharField(max_length=255, unique=True, verbose_name="Titre de l'article")
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    created_on = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False, verbose_name="Publié")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="author")
    is_featured = models.BooleanField(default=False, verbose_name="Présent sur la page d'accueil")
    summary = models.CharField(max_length=255, blank=True, null=True, verbose_name="Sommaire")
    content = models.TextField(blank=True, verbose_name="Contenu")
    thumbnail = models.ImageField(blank=True, upload_to=path_and_rename)
    tags = models.ManyToManyField(Tag, related_name='blogpost_tags')
    related_event = models.ForeignKey(Event, on_delete=models.SET_NULL, related_name='related_event', null=True, blank=True,  verbose_name="Évènement lié")
    linked_artists = models.ManyToManyField(Artist, related_name='linked_artists', blank=True, verbose_name="Artistes liés")
    comments = models.ManyToManyField(Comment, related_name='blogpost_comments', blank=True)


    class Meta:
        ordering = ["-created_on"]
        verbose_name = "Article"

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        return super().save(*args, **kwargs)
    
    @property
    def is_created_on_past_due(self):
        return date.today() > self.created_on.date()
    
    @property
    def is_last_updated_past_due(self):
        return date.today() > self.last_updated.date()
    
    def get_readtime(self):
      result = readtime.of_text(self.content)
      return result.text
    
    #Définir la redirection
    def get_absolute_url(self):
        return reverse("blog:post", kwargs={"slug": self.slug})