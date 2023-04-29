from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('projects/', views.projects_index, name='projects_index'),
    path('projects/<int:project_id>/', views.projects_detail, name='projects_detail'),
    path('projects/create/', views.ProjectCreate.as_view(), name="project_create"),
    path('projects/<int:pk>/update/', views.ProjectUpdate.as_view(), name="project_update"),
    path('projects/<int:pk>/delete/', views.ProjectDelete.as_view(), name="project_delete"),
    path('projects/<int:project_id>/add_photo/', views.add_photo, name='add_photo'),
    path('projects/<int:project_id>/add_timing/', views.add_timing, name='add_timing'),
    path('tutorials/', views.tutorial_search, name='tutorial_search'),
    path('tutorials/<str:video_id>/favorite/', views.add_favorite_video, name='add_favorite_video'),
    path('tutorials/<str:video_id>/unfavorite/', views.unfavorite_video, name='unfavorite_video'),
    path('tutorials/favorite/', views.favorite_videos, name='favorite_videos'),
    path('accounts/signup/', views.signup, name='signup')
]


urlpatterns += staticfiles_urlpatterns()
