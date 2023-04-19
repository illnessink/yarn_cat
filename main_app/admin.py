from django.contrib import admin
from .models import Project, Photo, Timing

# Register your models here.

admin.site.register(Project)
admin.site.register(Photo)
admin.site.register(Timing)
