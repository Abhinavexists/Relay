import datetime
import secrets
import base64
import os
from datetime import timezone, timedelta
import jwt

def generate_secret_key(length=32):
    """
    Generate a secure random secret key
    
    Args:
        length (int): Length of the key in bytes (default: 32)
        
    Returns:
        str: Base64 encoded secret key
    """
    # Generate random bytes
    random_bytes = secrets.token_bytes(length)
    
    # Convert to base64 string for easier handling
    base64_key = base64.b64encode(random_bytes).decode('utf-8')
    
    return base64_key

def generate_jwt(user_data, expiration_minutes=30):
    payload = {
        'sub': str(user_data.get('user_id', '')),
        'email': user_data.get('email', ''),
        'username': user_data.get('username', ''),
        'role': user_data.get('role', 'user'),
        # Use timezone-aware datetime
        'iat': datetime.datetime.now(timezone.utc),
        'exp': datetime.datetime.now(timezone.utc) + timedelta(minutes=expiration_minutes)
    }
    
    secret_key = os.getenv('JWT_SECRET_KEY')
    if not secret_key:
        secret_key = generate_secret_key()
    algorithm = os.getenv('JWT_ALGORITHM', 'HS256')
    
    # Use jwt directly
    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token, secret_key

# Example usage
if __name__ == "__main__":
    # Sample payload with correct keys
    user_data = {
        "user_id": 123,
        "email": "john@example.com",
        "username": "john_doe",
        "role": "user"
    }
    
    # Generate token with auto-generated secret key
    token, secret = generate_jwt(user_data)
    print(f"Generated Secret Key: {secret}")
    print(f"Generated JWT: {token}")
    
    # Verify token (optional)
    decoded = jwt.decode(token, secret, algorithms=["HS256"])
    print(f"Decoded JWT: {decoded}")