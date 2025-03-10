# Generated by Django 4.2.16 on 2025-03-04 10:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import nightlife.methods


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('artists', '0003_remove_artist_related_artists'),
        ('comments', '0002_comment_published'),
        ('tags', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='Titre')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('created_on', models.DateTimeField(blank=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('starts', models.DateTimeField(verbose_name='Début')),
                ('ends', models.DateTimeField(verbose_name='Fin')),
                ('published', models.BooleanField(default=False, verbose_name='Publié')),
                ('is_sponsored', models.BooleanField(default=False, verbose_name='Sponsorisé')),
                ('location', models.CharField(blank=True, max_length=255, null=True, verbose_name='Localisation')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Adresse')),
                ('town', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ville')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Prix')),
                ('content', models.TextField(blank=True, verbose_name='Contenu')),
                ('thumbnail', models.ImageField(blank=True, upload_to=nightlife.methods.PathAndRename('events/'))),
                ('artists', models.ManyToManyField(related_name='events', to='artists.artist')),
                ('comments', models.ManyToManyField(blank=True, related_name='event_comment', to='comments.comment')),
                ('interested', models.ManyToManyField(related_name='interested', to=settings.AUTH_USER_MODEL)),
                ('promoter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='promoter', to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(blank=True, related_name='event_tags', to='tags.tag')),
            ],
            options={
                'verbose_name': 'Event',
                'ordering': ['-created_on'],
            },
        ),
    ]
