import mysql.connector
from datetime import date

class DocumentDB:
    def __init__(self, db_config=None):
        """Initialize database connection"""
        if db_config is None:
            db_config = {
                'host': 'localhost',
                'user': 'root',
                'password': 'sql2707',
                'database': 'bits-ems'
            }
        
        try:
            self.db = mysql.connector.connect(**db_config)
            self.cursor = self.db.cursor()
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")
            raise

    def close(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()

    def drop_table(self):
        """Drop the Document table if it exists"""
        try:
            self.cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            self.cursor.execute("DROP TABLE IF EXISTS Document")
            self.cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            self.db.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error dropping table: {err}")
            return False

    def create_table(self):
        """Create the Document table"""
        try:
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Document (
                document_id BIGINT AUTO_INCREMENT PRIMARY KEY,
                EmpID INT NOT NULL,
                document_type VARCHAR(100) NOT NULL,
                file_path TEXT NOT NULL,
                upload_date DATE NOT NULL,
                Active BOOLEAN NOT NULL DEFAULT 1,
                CONSTRAINT document_empid_fk 
                    FOREIGN KEY (EmpID) REFERENCES Employee(EmpID)
            )
            """)
            self.db.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error creating table: {err}")
            return False

    def add_document(self, emp_id, document_type, file_path, upload_date=None):
        """Add a new document record"""
        try:
            if upload_date is None:
                upload_date = date.today()
            
            sql = """
            INSERT INTO Document (EmpID, document_type, file_path, upload_date)
            VALUES (%s, %s, %s, %s)
            """
            values = (emp_id, document_type, file_path, upload_date)
            
            self.cursor.execute(sql, values)
            self.db.commit()
            return self.cursor.lastrowid
        except mysql.connector.Error as err:
            print(f"Error adding document: {err}")
            return None

    def get_document(self, document_id):
        """Get document by ID"""
        try:
            sql = "SELECT * FROM Document WHERE document_id = %s"
            self.cursor.execute(sql, (document_id,))
            result = self.cursor.fetchone()
            
            if result:
                columns = [desc[0] for desc in self.cursor.description]
                return dict(zip(columns, result))
            return None
        except mysql.connector.Error as err:
            print(f"Error getting document: {err}")
            return None

    def get_employee_documents(self, emp_id, active_only=True):
        """Get all documents for an employee"""
        try:
            if active_only:
                sql = "SELECT * FROM Document WHERE EmpID = %s AND Active = 1"
            else:
                sql = "SELECT * FROM Document WHERE EmpID = %s"
            
            self.cursor.execute(sql, (emp_id,))
            results = self.cursor.fetchall()
            
            columns = [desc[0] for desc in self.cursor.description]
            return [dict(zip(columns, row)) for row in results]
        except mysql.connector.Error as err:
            print(f"Error getting documents: {err}")
            return []

    def update_document(self, document_id, **kwargs):
        """Update document information"""
        try:
            allowed_fields = ['document_type', 'file_path', 'upload_date', 'Active']
            updates = []
            values = []
            
            for field, value in kwargs.items():
                if field in allowed_fields:
                    updates.append(f"{field} = %s")
                    values.append(value)
            
            if not updates:
                return False
            
            values.append(document_id)
            sql = f"UPDATE Document SET {', '.join(updates)} WHERE document_id = %s"
            
            self.cursor.execute(sql, values)
            self.db.commit()
            return self.cursor.rowcount > 0
        except mysql.connector.Error as err:
            print(f"Error updating document: {err}")
            return False

    def delete_document(self, document_id):
        """Delete a document"""
        try:
            sql = "DELETE FROM Document WHERE document_id = %s"
            self.cursor.execute(sql, (document_id,))
            self.db.commit()
            return self.cursor.rowcount > 0
        except mysql.connector.Error as err:
            print(f"Error deleting document: {err}")
            return False

    def deactivate_document(self, document_id):
        """Deactivate a document (soft delete)"""
        return self.update_document(document_id, Active=0)
    
    def get_employee_image(self, emp_id):
        query = """
            SELECT file_path
            FROM document
            WHERE EmpID = %s AND document_type = 'image'
            ORDER BY upload_date DESC
            LIMIT 1
        """
        self.cursor.execute(query, (emp_id,))
        row = self.cursor.fetchone()
        return row[0] if row else None

# For other pages to use:
    def get_document_db():
        """Get DocumentDB instance"""
        return DocumentDB()