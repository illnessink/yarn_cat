import requests
import os
from isodate import parse_duration
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Project, Photo, Video
from .forms import TimingForm
from django.contrib.auth.forms import UserCreationForm

import uuid
import boto3

S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET = 'yarncat'


# Create your views here.

@login_required
def tutorial_search(request):
    videos = []

    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        search_params = {
            'part': 'snippet',
            'q': request.POST['search'],
            'key' : os.environ.get("YOUTUBE_DATA_API_KEY"),
            'maxResults': 10,
            'type': 'video',
        }
        video_ids = []
        r = requests.get(search_url, params=search_params)
        if not r:
            return render(request, 'tutorials/search.html', {'error': 'No results found. Please try again.'})
        results = r.json()['items']

        for result in results:
            video_ids.append(result['id']['videoId'])
        
        video_params = {
            'part': 'snippet, contentDetails',
            'key' : os.environ.get("YOUTUBE_DATA_API_KEY"),
            'id': ','.join(video_ids),
            'maxResults': 10,
        }

        r = requests.get(video_url, params=video_params)
        results = r.json()['items']

        for result in results:
            if Video.objects.filter(url=f'https://www.youtube.com/embed/{ result["id"] }').exists():
                favorite = True
            else:
                favorite = False
            video_data = {
                'title' : result['snippet']['title'],
                'id' : result['id'],
                'url': f'https://www.youtube.com/embed/{ result["id"] }',
                'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'thumbnail' : result['snippet']['thumbnails']['high']['url'],
                'favorite': favorite,
            }

            videos.append(video_data)

    context = {
        'videos': videos
    }

    return render(request, 'tutorials/search.html', context)

@login_required
def add_favorite_video(request, video_id):
    video = Video.objects.create(
        favorited_by = request.user,
        url = f'https://www.youtube.com/embed/{ video_id }',
    )
    return redirect('tutorial_search')

@login_required
def unfavorite_video(request, video_id):
    video = Video.objects.filter(
         favorited_by = request.user,
        id = video_id,
    ).delete()
    # video = Video.objects.get(id=video_id)
    # video.favorited_by.remove(request.user)
    return redirect('favorite_videos')

@login_required
def favorite_videos(request):
    videos = Video.objects.filter(favorited_by=request.user)
    for video in videos:
        print(video.id)
    return render(request, 'tutorials/favorite.html', {'videos': videos})

def home(request):
   return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def projects_index(request):
    projects = Project.objects.filter(user=request.user)
    return render(request, 'projects/index.html', {'projects': projects})

@login_required
def projects_detail(request, project_id):
    project = Project.objects.get(id=project_id)
    timing_form = TimingForm()
    timings = project.timing_set.all()
    total_time = project.project_total_time()
    return render(request, 'projects/detail.html', {
        'project': project,
        'timing_form': timing_form,
        'timings': timings,
        'total_time': total_time
        })

def add_timing(request, project_id):
    form = TimingForm(request.POST)
    if form.is_valid():
        new_timing = form.save(commit=False)
        new_timing.project_id = project_id
        new_timing.save()
    return redirect('projects_detail', project_id=project_id)

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