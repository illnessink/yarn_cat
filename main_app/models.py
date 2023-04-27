from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import timedelta

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=100)
    tools = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    description = models.TextField(max_length=400)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('projects_detail', kwargs={'project_id': self.id})
    
    def project_total_time(self):
        timings = Timing.objects.filter(project=self)
        total_time = sum([t.time_spent for t in timings], timedelta())
        #convert to string
        total_time = str(total_time)
        #split string on colons
        total_time = total_time.split(':')
        #format string for days hours and minutes
        total_time = f"{total_time[1]} hours and {total_time[2]} minutes"
        return total_time
    

class Photo(models.Model):
    url = models.CharField(max_length=200)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for project_id: {self.project_id} @{self.url}"
    

class Timing(models.Model):
    date = models.DateField('Date as YYYY-MM-DD')
    time_spent = models.DurationField('time spent - in minutes')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.time_spent} spent on {self.date}"
    
    class Meta:
        ordering = ('-date',)


class Video(models.Model):
    url = models.URLField()
    favorited_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Video {self.url} favorited by {User}"