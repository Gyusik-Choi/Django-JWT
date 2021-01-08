import bcrypt
import jwt
import re
from datetime import datetime, timedelta
from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer, UsernameSerializer
from signup.settings import SECRET_KEY_JWT, ALGORITHM

# password1, password2의 일치여부는 프론트에서 처리하자
# password1의 길이를 체크(8자 이상)
# password1의 영문, 숫자, 특수문자 사용여부 체크(정규표현식)
# password1의 암호화를 진행한다
@api_view(['POST'])
def signup(request):
    User = get_user_model()
    user_input = request.data

    if len(user_input['password']) < 8:
        return Response({'message', '비밀번호를 8자 이상으로 작성해주세요'})

    comp = re.compile('[A-Za-z0-9!@#$%^&*?]')
    mat = re.match(comp, user_input['password'])
    if not mat:
        return Response({'message', '비밀번호는 대문자 1개 이상, 소문자 1개 이상, 특수문자 1개 이상, 숫자 1개 이상을 포함해야 합니다'})
    
    password = user_input['password']
    
    # 문자열에서 바이트형태로 변환돼야 한다
    encoded_password = password.encode('utf-8')
    safe_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())

    serializer = UserSerializer(data=user_input)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        password_crypt(user_input['username'], safe_password)
    return Response({'message', '회원가입이 완료됐습니다'})


def password_crypt(new_username, new_password):
    # 바이트형태를 다시 문자열로 변환한다
    new_password = new_password.decode('utf-8')
    User = get_user_model()
    user = User.objects.get(username=new_username)
    user.password = new_password
    user.save()
    return


@api_view(['GET'])
def username_check(request):
    User = get_user_model()
    if User.objects.filter(username = user_input['username']).exists():
        return Response({'message', '존재하는 닉네임입니다'})
    else:
        return Response({'message', '사용가능한 닉네임입니다'})


@api_view(['GET'])
def email_check(request):
    User = get_user_model()
    if User.objects.filter(email = user_input['email']).exists():
        return Response({'message', '존재하는 이메일입니다'})
    else:
        return Response({'message', '사용가능한 이메일입니다'})


@api_view(['POST'])
def login(request):
    user_input = request.data
    print(user_input)
    User = get_user_model()
    if User.objects.filter(email=user_input['email']).exists():
        user = User.objects.get(email=user_input['email'])
        if bcrypt.checkpw(user_input['password'].encode('utf-8'), user.password.encode('utf-8')):
            access_token = prepare_encode_jwt_access(user_input['username'])
            # refresh_token = prepare_encode_jwt_refresh(user_input['username'])
            # user.refresh_token = refresh_token
            user.save()
            return Response({
                'access_token': access_token, 
                # 'refresh_token': refresh_token,
                'message': '로그인에 성공했습니다'
            })
        else:
            return Response({'message', '비밀번호를 확인해주세요'})
    else:
        return Response({'message', '존재하지 않는 아이디입니다'})


def prepare_encode_jwt_access(username):
    iat = datetime.now()
    exp = iat + timedelta(hours=1)

    data = {
        "iat": iat.timestamp(),
        "exp": exp.timestamp(),
        "aud": username,
    }
    return encode_jwt_access(data)


def encode_jwt_access(data):
    return jwt.encode(data, SECRET_KEY_JWT, algorithm=ALGORITHM).decode("utf-8")


def prepare_encode_jwt_refresh(username):
    iat = datetime.now()
    exp = iat + timedelta(days=7)

    data = {
        "iat": iat.timestamp(),
        "exp": exp.timestamp(),
        "aud": username,
    }
    return encode_jwt_refresh(data)


def encode_jwt_refresh(data):
    return jwt.encode(data, SECRET_KEY_JWT, algorithm=ALGORITHM).decode("utf-8")