from django.contrib import admin
from .models import HashBlock
@admin.register(HashBlock)
class HashBlockAdmin(admin.ModelAdmin):
    list_display = ['block_index', 'user', 'record_type', 'timestamp']
    list_filter = ['record_type']
