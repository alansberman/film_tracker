from django.contrib import admin

from .models import Film, CrewCredit, Keyword, Genre, ActingCredit, Recommendation

admin.site.register(Film)
admin.site.register(CrewCredit)
admin.site.register(ActingCredit)
admin.site.register(Keyword)
admin.site.register(Genre)
admin.site.register(Recommendation)
