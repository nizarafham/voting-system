from django.core.mail import send_mail
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

import random
import string
from .models import User, Token, Candidate
from .serializers import UserSerializer, TokenSerializer, CandidateSerializer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer

@api_view(['POST'])
@renderer_classes([JSONRenderer]) 
def login(request):
    nim = request.data.get('nim')
    email = request.data.get('email')

    if not nim or not email:
        return Response({'error': 'NIM dan email harus diisi'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)

        created = False
    except User.DoesNotExist:
        user = User.objects.create(nim=nim, email=email)
        created = True

    token = ''.join(random.choices(string.ascii_letters + string.digits, k=20))

    try:
        Token.objects.filter(user=user).delete()

        Token.objects.create(user=user, token=token)
    except IntegrityError:
        return Response({'error': 'Gagal menyimpan token'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

    return Response(
        {'message': 'Token sent to your email', 'created': created},
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
@renderer_classes([JSONRenderer])
def verify_token(request):
    token = request.data.get('token')
    try:
        token_obj = Token.objects.get(token=token)
        user = token_obj.user
        return Response({'message': 'Token verified', 'user': UserSerializer(user).data}, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response({'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@renderer_classes([JSONRenderer])
def vote(request):
    user_id = request.data.get('user_id')
    candidate_id = request.data.get('candidate_id')
    user = User.objects.get(id=user_id)
    if user.has_voted:
        return Response({'message': 'You have already voted'}, status=status.HTTP_400_BAD_REQUEST)
    user.has_voted = True
    user.save()
    candidate = Candidate.objects.get(id=candidate_id)
    return Response({'message': 'Vote successful'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def candidates(request):
    candidates = Candidate.objects.all()
    serializer = CandidateSerializer(candidates, many=True)
    return Response(serializer.data)

def home(request):
    return JsonResponse({'message': 'Welcome to the Voting System API!'})