# Empty.py - Fixed version
from DB_Service.DocumentDB import DocumentDB  # Import the class, not the module

def setup_document_table():
    """Create or recreate the document table"""
    db = DocumentDB()  # Now this will work
    
    print("Choose action:")
    print("1. Create table (if not exists)")
    print("2. Drop and recreate table")
    print("3. Drop table only")
    
    choice = input("Enter choice (1-3): ")
    
    if choice == "1":
        if db.create_table():
            print("Table created successfully!")
    elif choice == "2":
        db.drop_table()
        if db.create_table():
            print("Table recreated successfully!")
            
    elif choice == "3":
        if db.drop_table():
            print("Table dropped successfully!")
    
    db.close()

if __name__ == "__main__":
    setup_document_table()