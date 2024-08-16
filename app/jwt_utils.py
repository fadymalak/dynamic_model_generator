import jwt
import datetime

def generate_jwt_token(payload, secret_key, expiration_minutes=60):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=expiration_minutes)
    payload['exp'] = expiration
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token
