from django.contrib import admin

from .models import Apartment


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', 'area', 'rooms', 'floor', 'price', 'status')
    list_filter = ('status', 'rooms', 'floor')
    search_fields = ('title', 'description')
