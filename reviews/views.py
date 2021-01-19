from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Review
from .serializers import ReviewSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from signup.utils import login_decorator

@api_view(['POST'])
@login_decorator
def create_review(request):
    serializer = ReviewSerializer(data=request.data)
    print(request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
    return Response(serializer.data)
