from django.contrib import admin

# Register your models here.
from .models import * #imporata nossos models
admin.site.register(Usuario)