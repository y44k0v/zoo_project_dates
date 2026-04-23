from django.contrib import admin
from .models import Animal

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'weight', 'born_in_captivity', 'date_added']
    list_filter = ['born_in_captivity', 'date_added']
    search_fields = ['name']