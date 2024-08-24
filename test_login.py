import requests

url = 'http://localhost:8000/api/login/'  # Adjust the URL if necessary
data = {
    'username': 'testuser',  # Replace with a valid username
    'password': 'testpassword'  # Replace with the corresponding password
}

response = requests.post(url, json=data)
print(response.status_code)
print(response.json())
