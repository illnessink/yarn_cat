from django.urls import path
from . import views

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
    path('accounts/signup/', views.signup, name='signup')
]



