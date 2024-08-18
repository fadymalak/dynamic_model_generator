import os
import sys
import django

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paymob.settings')
django.setup()

from django.contrib.auth import get_user_model
from jwt_generator import generate_jwt_token

def test_generate_jwt_token():
    User = get_user_model()
    user = User.objects.create_user(username='testuser', password='testpassword')
    tokens = generate_jwt_token(user)
    
    assert 'refresh' in tokens
    assert 'access' in tokens
    assert tokens['refresh'] is not None
    assert tokens['access'] is not None

if __name__ == "__main__":
    test_generate_jwt_token()
    print("JWT token generation test passed.")
