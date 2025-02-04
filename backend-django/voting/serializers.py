from rest_framework import serializers
from .models import User, Token, Candidate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nim', 'email']

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['user', 'token']

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['id', 'name', 'vice_name', 'vision', 'mission']