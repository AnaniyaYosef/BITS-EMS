
import bcrypt


def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    try:
        # Generate a salt and hash the password
        salt = bcrypt.gensalt()
        password_bytes = password.encode('utf-8')
        hashed_password = bcrypt.hashpw(password_bytes, salt)
        return hashed_password.decode('utf-8')
    except (ValueError, TypeError) as e:
        print(f"Error hashing password: {e}")
        return ""


def verify_password(stored_password_hash: str, provided_password: str) -> bool:
    """Verify a password against a stored bcrypt hash"""
    try:
        # Check if stored hash is a valid bcrypt hash format
        if not stored_password_hash or len(stored_password_hash) < 60 or not stored_password_hash.startswith('$2b$') and not stored_password_hash.startswith('$2a$'):
            print("Invalid bcrypt hash format")
            return False
            
        # Convert the stored hash from string to bytes
        stored_hash = stored_password_hash.encode('utf-8')
        # Convert the provided password to bytes
        password_bytes = provided_password.encode('utf-8')
        
        # Check if the password matches the hash
        return bcrypt.checkpw(password_bytes, stored_hash)
    except (ValueError, TypeError) as e:
        print(f"Error verifying password: {e}")
        return False