from django.contrib import admin

# Register your models here.
from .models import Show, ActingCredit, CrewCredit, Genre, Season, Episode, Recommendation

admin.site.register(Show)
admin.site.register(ActingCredit)
admin.site.register(CrewCredit)
admin.site.register(Genre)
admin.site.register(Season)
admin.site.register(Episode)
