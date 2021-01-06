import jwt                                                
import json
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from .settings import SECRET_KEY_JWT, ALGORITHM

def login_decorator(func):
    def wrapper(request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization')
            payload = jwt.decode(access_token, SECRET_KEY_JWT, algorithms=ALGORITHM, audience="abcde")
            print(payload)
            User = get_user_model()
            user = User.objects.get(username=payload['aud'])
            request.user = user
            return func(request, *args, **kwargs)

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message' : 'INVALID_TOKEN' }, status=400)

    return wrapper