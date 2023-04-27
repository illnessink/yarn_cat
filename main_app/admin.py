from django.contrib import admin
from .models import Project, Photo, Timing, Video

# Register your models here.

admin.site.register(Project)
admin.site.register(Photo)
admin.site.register(Timing)
admin.site.register(Video)
