"""
Password utility functions for hashing and verification
"""
import bcrypt


def verify_password(stored_password_hash: str, provided_password: str) -> bool:
    """
    Verify a password against a stored hash.
    
    Args:
        stored_password_hash: The hashed password stored in the database
        provided_password: The plaintext password to verify
        
    Returns:
        bool: True if the password matches, False otherwise
    """
    try:
        # Convert the stored hash from string to bytes
        stored_hash = stored_password_hash.encode('utf-8')
        # Convert the provided password to bytes
        password_bytes = provided_password.encode('utf-8')
        
        # Check if the password matches the hash
        return bcrypt.checkpw(password_bytes, stored_hash)
    except (ValueError, TypeError) as e:
        print(f"Error verifying password: {e}")
        return False