from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'pollapp'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('createdPolls/', views.ListView.as_view(), name='createdPolls'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('createPoll/', views.CreatePoll.as_view(), name='createPoll'),
    path('<int:pk>/choice', views.createChoice, name='createChoice'),
    path('userPolls/', views.UserPolls.as_view(), name='userPolls'),
]