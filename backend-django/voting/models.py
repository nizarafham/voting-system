from django.db import models

class PendingUser(models.Model):
    nim = models.CharField(max_length=9, unique=True)
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    attempts = models.IntegerField(default=0)  # Menyimpan jumlah percobaan verifikasi

    def __str__(self):
        return f"{self.nim} - {self.email} (Attempts: {self.attempts})"
    
class User(models.Model):
    nim = models.CharField(max_length=9, unique=True)
    email = models.EmailField(unique=True)
    has_voted = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    last_activity = models.DateTimeField(auto_now=True)

# class Token(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     token = models.CharField(max_length=100)
#     created_at = models.DateTimeField(auto_now_add=True)

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    vice_name = models.CharField(max_length=100)
    vision = models.TextField()
    mission = models.TextField()

class Vote(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # One user, one vote
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # Menyimpan waktu voting

    def __str__(self):
        return f"{self.user.nim} voted for {self.candidate.name}"