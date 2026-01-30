# DB_Service/register.py
import os
import sys
import getpass

# Add project root to sys.path so utils can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from DB_Service.Login_db import LoginDB
from utils.password_utils import hash_password

def main():
    db = LoginDB()

    # Ensure database connection
    if not db.connect():
        print("Failed to connect to the database.")
        return

    # Create UserAccount table if it doesn't exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS UserAccount (
        user_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
        userName VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        Active BOOLEAN NOT NULL DEFAULT 1
    );
    """
    db.cursor.execute(create_table_query)
    db.connection.commit()

    print("=== Register a new user ===")
    #username = input("Username: ").strip()
    username = "Admin"

    # Check if username already exists
    db.cursor.execute("SELECT * FROM UserAccount WHERE userName = %s", (username,))
    if db.cursor.fetchone():
        print(f"Username '{username}' already exists!")
        db.close()
        return

    # password = getpass.getpass("Password: ").strip()
    # confirm = getpass.getpass("Confirm Password: ").strip()
    password = "Admin"
    confirm = "Admin"


    if password != confirm:
        print("Passwords do not match!")
        db.close()
        return

    # Hash password before saving
    hashed_password = hash_password(password)

    # Insert into database
    try:
        db.cursor.execute(
            "INSERT INTO UserAccount (userName, password, Active) VALUES (%s, %s, %s)",
            (username, hashed_password, True)
        )
        db.connection.commit()
        print(f"User '{username}' registered successfully!")
    except Exception as e:
        print(f"Registration failed: {e}")
        db.connection.rollback()

    db.close()


if __name__ == "__main__":
    main()