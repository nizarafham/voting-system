from django.db import models

class User(models.Model):
    nim = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    has_voted = models.BooleanField(default=False)

class Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    vice_name = models.CharField(max_length=100)
    vision = models.TextField()
    mission = models.TextField()