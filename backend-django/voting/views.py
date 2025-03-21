import random
import string
import re
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .models import User, Candidate, Vote, PendingUser #,Token
from .serializers import UserSerializer, CandidateSerializer #, TokenSerializer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer

def home(request):
    return JsonResponse({
        'message': 'Welcome to the Voting System API!',
        'user': {
            'name': 'nizar',
        }
    })

@api_view(['POST'])
@renderer_classes([JSONRenderer])
def login(request):
    nim = request.data.get('nim')
    email = request.data.get('email')

    if not nim or not nim.isdigit() or len(nim) != 9:
        return Response({'error': 'NIM harus terdiri dari 9 angka'}, status=status.HTTP_400_BAD_REQUEST)

    email_regex = r'^[0-9]{9}@student\.universitaspertamina\.ac\.id$'
    if not email or not re.match(email_regex, email):
        return Response({'error': 'Email harus sesuai format: nim@student.universitaspertamina.ac.id'}, status=status.HTTP_400_BAD_REQUEST)

    if not email.startswith(nim):
        return Response({'error': 'NIM di email tidak cocok dengan NIM yang diinputkan'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(nim=nim).exists() or User.objects.filter(email=email).exists():
        return Response({'error': 'NIM atau Email sudah digunakan'}, status=status.HTTP_400_BAD_REQUEST)

    token = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

    try:
        with transaction.atomic():
            pending_user = PendingUser.objects.select_for_update().filter(nim=nim).first()

            if pending_user:
                pending_user.delete()

            PendingUser.objects.create(nim=nim, email=email, token=token)
    except Exception as e:
        return Response({'error': f'Gagal menyimpan pending user: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        send_mail(
            'Your Voting Token',
            f'Your token is: {token}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
    except Exception as e:
        return Response({'error': f'Gagal mengirim email: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'message': 'Token sent to your email'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@renderer_classes([JSONRenderer])
def verify_token(request):
    token = request.data.get('token')
    nim = request.data.get('nim')
    
    try:
        pending_user = PendingUser.objects.get(token=token, nim=nim)
    except PendingUser.DoesNotExist:
        return Response({'error': 'Token tidak valid'}, status=status.HTTP_400_BAD_REQUEST)

    if token != pending_user.token:
        pending_user.attempts += 1
        pending_user.save()

        if pending_user.attempts >= 2:
            pending_user.delete()
            return Response({'error': 'Terlalu banyak percobaan, silakan login ulang'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error': 'Token salah, coba lagi'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create(nim=pending_user.nim, email=pending_user.email, is_verified=True)

    pending_user.delete()

    return Response({'message': 'Token verified', 'user': {'nim': user.nim, 'email': user.email}}, status=status.HTTP_200_OK)

@api_view(['POST'])
@renderer_classes([JSONRenderer])
def vote(request):
    nim = request.data.get('nim')
    candidate_id = request.data.get('candidate_id')

    try:
        user = User.objects.get(nim=nim) 
        if user.has_voted:
            return Response({'message': 'You have already voted'}, status=status.HTTP_400_BAD_REQUEST)
        
        candidate = Candidate.objects.get(id=candidate_id)
        user.has_voted = True
        user.last_activity = timezone.now()
        user.save()
        
        Vote.objects.create(user=user, candidate=candidate)
        
        return Response({'message': 'Vote successful'}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Candidate.DoesNotExist:
        return Response({'message': 'Candidate not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def candidates(request):
    candidates = Candidate.objects.all()
    serializer = CandidateSerializer(candidates, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def session(request):
    return Response({'message': 'Session endpoint'}, status=status.HTTP_200_OK)



from rest_framework import viewsets
from .models import Candidate
from .serializers import CandidateSerializer

class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer