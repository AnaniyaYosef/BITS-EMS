import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from utils.password_utils import verify_password, hash_password

# Load environment variables
load_dotenv()


class LoginDB:
    """Database service for login operations"""

    def __init__(self):
        self.connection = None
        self.cursor = None
        self.connect()
        self.create_user_table()

    def connect(self) -> bool:
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv("DB_HOST", "localhost"),
                database=os.getenv("DB_NAME", "bits_ems"),
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASSWORD", "")
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                return True
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return False

    def create_user_table(self):
        """Create UserAccount table if it doesn't exist"""
        if not self.cursor:
            print("Cannot create table: No database connection")
            return
        query = """
        CREATE TABLE IF NOT EXISTS UserAccount (
            user_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
            userName VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            Active BOOLEAN NOT NULL DEFAULT 1
        );
        """
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except mysql.connector.Error as e:
            print(f"Error creating UserAccount table: {e}")

    def register_user(self, username: str, password: str) -> bool:
        """Register a new user (for terminal registration only)"""
        try:
            hashed = hash_password(password)
            query = "INSERT INTO UserAccount (userName, password, Active) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (username, hashed, True))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error registering user: {e}")
            return False

    def authenticate_user(self, username: str, password: str):
        """Authenticate user credentials"""
        if not self.connection or not self.connection.is_connected():
            if not self.connect():
                return None
        try:
            query = "SELECT user_id, userName, password, Active FROM UserAccount WHERE userName=%s AND Active=1"
            self.cursor.execute(query, (username,))
            user = self.cursor.fetchone()
            if user and verify_password(user["password"], password):
                # Return minimal user info
                return {
                    "id": user["user_id"],
                    "username": user["userName"],
                    "status": "active" if user["Active"] else "inactive"
                }
            return None
        except Error as e:
            print(f"Error authenticating user: {e}")
            return None

    def close(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            if self.cursor:
                self.cursor.close()
            self.connection.close()