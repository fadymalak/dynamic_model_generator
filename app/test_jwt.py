from utils import generate_jwt_token
# from rest_framework import serializers
# Sample payload and secret key
payload = {"user_id": 123, "username": "testuser"}
secret_key = "my_secret_key"

# Generate JWT token
token = generate_jwt_token(payload, secret_key)
print("Generated JWT Token:", token)
