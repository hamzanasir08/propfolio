

from django.contrib import admin
from .models import City, Town

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('cityID', 'city_name')
    search_fields = ('city_name',)

@admin.register(Town)
class TownAdmin(admin.ModelAdmin):
    list_display = ('townID', 'town_name', 'city')
    search_fields = ('town_name',)
    list_filter = ('city',)