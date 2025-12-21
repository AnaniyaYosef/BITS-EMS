"""
Database service for login functionality
"""
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LoginDB:
    """Database service for login operations"""
    
    def __init__(self):
        self.connection = None
        self.cursor = None
        
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                database=os.getenv('DB_NAME', 'bits_ems'),
                user=os.getenv('DB_USER', 'root'),
                password=os.getenv('DB_PASSWORD', '')
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                return True
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return False
    
    def authenticate_user(self, username, password):
        """Authenticate user credentials"""
        if not self.connection or not self.connection.is_connected():
            if not self.connect():
                return None
        
        try:
            query = """
                SELECT id, username, full_name, role, email, status 
                FROM users 
                WHERE username = %s AND password = %s AND status = 'active'
            """
            self.cursor.execute(query, (username, password))
            result = self.cursor.fetchone()
            return result
        except Error as e:
            print(f"Error authenticating user: {e}")
            return None
    
    def close(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
