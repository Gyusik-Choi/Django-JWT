# JWT

## access_token

### encoding

```python
def prepare_encode_jwt_access(username):
    iat = datetime.now()
    exp = iat + timedelta(hours=1)

    data = {
        "iat": iat.timestamp(),
        "exp": exp.timestamp(),
        "aud": username,
    }
    return encode_jwt_access(data)
```

"aud"를 활용했다면 decoding시에 주의해야한다.



### decoding

pyjwt(jwt)의 내부 코드의 일부다

```python
def decode(self,
               jwt,  # type: str
               key='',   # type: str
               verify=True,  # type: bool
               algorithms=None,  # type: List[str]
               options=None,  # type: Dict
               **kwargs):
	pass

def _validate_claims(self, payload, options, audience=None, issuer=None,
                         leeway=0, **kwargs):
	pass

def _validate_aud(self, payload, audience):
    if audience is None and 'aud' in payload:
        # Application did not specify an audience, but
        # the token has the 'aud' claim
        raise InvalidAudienceError('Invalid audience')
```

_validate_claims 함수에서 audience=None으로 되어있다.

즉 decode를 호출할 때 options나 **kwargs에 audience 정보를 직접 기재하지 않으면 계속 audience는 None이기 때문에 InvalidAudienceError가 계속 발생하게 된다.

이 문제 때문에 한참을 삽질을 거듭했다.

사실 내부 코드가 너무 어려울 것 같아서 열어볼 엄두를 못냈는데 터미널에 찍힌 위치를 기반으로 하나씩 추적해보니 생각보다는 코드가 어렵지 않았다.



```python
access_token = request.headers.get('Authorization')
audience_name = request.data['username']
payload = jwt.decode(access_token, SECRET_KEY_JWT, algorithms=ALGORITHM, audience=audience_name)
```

access_token을 바탕으로 decoding을 요청하게 되는 함수의 일부분이다.

그리고 한가지 특이했던 점은 pyjwt 내부 코드의 decode 함수 부분의 파라미터에서 algorithms라고 적혀있으나 요청할때 인자를 algorithm으로 보내도 동작에는 문제가 없었다.



추가해야할 부분은 데코레이터에서 토큰 만료를 리턴하게 되면 클라이언트에서 토큰 재발급을 위한 요청을 넣는데 이를 어떻게 처리할 것인지와 만약에 refresh token을 기반으로 access token을 재발급한다고 하면 refresh token마저 만료일때 어떻게 처리할지다.



참고

https://github.com/jpadilla/pyjwt/issues/120

