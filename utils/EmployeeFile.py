import os
import shutil
from datetime import date
from DB_Service.DocumentDB import DocumentDB  # Ensure this path is correct

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MainFolder = os.path.join(BASE_DIR, "Document")

def CreateFolder(EmployeeId):
    EmployeeFolder = f"{EmployeeId}_File"
    path = os.path.join(MainFolder, EmployeeFolder)
    os.makedirs(path, exist_ok=True)
    return path

def _save_single_file(employee_folder, source_path, new_name):
    if not source_path or not os.path.exists(source_path):
        return None

    _, ext = os.path.splitext(source_path)
    new_filename = f"{new_name}{ext}"
    destination = os.path.join(employee_folder, new_filename)

    shutil.copy(source_path, destination)
    return destination

def SaveEmpFile(EmployeeId, files):
    # 1. Create the physical folder
    employee_folder = CreateFolder(EmployeeId=EmployeeId)
    saved_paths = {}
    
    # 2. Initialize Database connection
    db = DocumentDB()

    # Define the files to process
    file_types = ["image", "cv", "certificate", "id", "contract"]

    for f_type in file_types:
        source = files.get(f_type)
        if source:
            # Save physically
            dest = _save_single_file(employee_folder, source, f"{EmployeeId}_{f_type}")
            
            if dest:
                saved_paths[f_type] = dest
                # 3. Save to Database immediately
                db.add_document(
                    emp_id=EmployeeId,
                    document_type=f_type,
                    file_path=dest,
                    upload_date=date.today()
                )

    # 4. Close DB connection
    db.close()
    return saved_paths