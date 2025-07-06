from django.contrib import admin

# Register your models here.
from .models import Review

class ReviewAdmin(admin.ModelAdmin):
    date_hierarchy = 'creation_date'
    list_display = ('stars', 'message', 'creation_date',)
    empty_value_display = ' - '

admin.site.register(Review, ReviewAdmin)