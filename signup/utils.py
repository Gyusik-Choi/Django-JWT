import jwt                                                
import json
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from .settings import SECRET_KEY_JWT, ALGORITHM

def login_decorator(func):
    def wrapper(request, *args, **kwargs):
        try:
            access_check = False
            refresh_check = False

            User = get_user_model()

            access_token = request.headers.get('Authorization')
            audience_name = request.data['username']

            payload = jwt.decode(access_token, SECRET_KEY_JWT, algorithms=ALGORITHM, audience=audience_name)
            access_check = True

            user = User.objects.get(username=payload['aud'])

            # refresh_token이 없으면 로그아웃 상태인 유저다
            refresh_token = user.refresh_token
            if refresh_token == None:
                return JsonResponse({'message': '로그인해주세요'})
            
            payload_refresh = jwt.decode(refresh_token, SECRET_KEY_JWT, algorithms=ALGORITHM, audience=audience_name)
            refresh_check = True

            request.user = user
            if access_check and refresh_check:
                return func(request, *args, **kwargs)
            elif access_check and not refresh_check:
                return JsonResponse({'message': 'Invalid refresh token'})
            else:
                return JsonResponse({'message': 'Invalid access token'})

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message' : 'INVALID_TOKEN' }, status=400)
        except jwt.exceptions.ExpiredSignatureError:
            return JsonResponse({'message': 'Signature has expired'})

    return wrapper