"""
URL configuration for voting_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from voting import views
from rest_framework.routers import DefaultRouter
from voting.views import CandidateViewSet


router = DefaultRouter()
# router.register(r'candidates', CandidateViewSet)

urlpatterns = [
    path('', views.home),
    path('login/', views.login, name='login'),
    path('verify_token/', views.verify_token, name='verify_token'),
    path('vote/', views.vote, name='vote'),
    path('candidates/', views.candidates, name='candidates'),
    # path('api/', include(router.urls)),
]