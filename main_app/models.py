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
    

class Photo(models.Model):
    url = models.CharField(max_length=200)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for project_id: {self.project_id} @{self.url}"
    

class Timing(models.Model):
    date = models.DateField('timing date')
    time_spent = models.DurationField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.time_spent} spent on {self.date}"
    
    class Meta:
        ordering = ('-date',)

    def project_total_time(self):
        timings = Timing.objects.filter(project=self.project)
        total_time = sum([t.time_spent for t in timings], timedelta())
        return total_time