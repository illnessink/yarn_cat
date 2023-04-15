from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Project, Photo
from django.contrib.auth.forms import UserCreationForm

import uuid
import boto3

S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET = 'yarncat'


# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def projects_index(request):
    projects = Project.objects.filter(user=request.user)
    return render(request, 'projects/index.html', {'projects': projects})

def projects_detail(request, project_id):
    project = Project.objects.get(id=project_id)
    return render(request, 'projects/detail.html', {'project': project})

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('projects_index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form, 'error': error_message})

def add_photo(request, project_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            Photo.objects.create(url=url, project_id=project_id)
        except Exception as error:
            print('An error occurred uploading file to S3: ', error)

    return redirect('projects_detail', project_id=project_id)

class ProjectCreate(LoginRequiredMixin, CreateView):
    model = Project
    fields = ('name', 'type', 'tools', 'description')
    template_name = 'projects/project_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class ProjectUpdate(LoginRequiredMixin, UpdateView):
    model = Project
    fields = ('name', 'type', 'tools', 'description')
    template_name = 'projects/project_form.html'

class ProjectDelete(LoginRequiredMixin, DeleteView):
    model = Project
    success_url = '/projects/'
    template_name = 'projects/project_confirm_delete.html'