from django.contrib import admin
from .models import *

admin.site.register(Genre)
admin.site.register(Animeshnik)
admin.site.register(Moderator)
admin.site.register(Anime)
admin.site.register(AnimeHistory)
admin.site.register(UserAnimeStatus)