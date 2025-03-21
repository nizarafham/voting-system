
from django.urls import path
from voting import views
from rest_framework.routers import DefaultRouter
from voting.views import CandidateViewSet


router = DefaultRouter()

urlpatterns = [
    path('', views.home),
    path('login/', views.login, name='login'),
    path('verify_token/', views.verify_token, name='verify_token'),
    path('vote/', views.vote, name='vote'),
    path('candidates/', views.candidates, name='candidates'),
    path('session/', views.session, name='session'),
]