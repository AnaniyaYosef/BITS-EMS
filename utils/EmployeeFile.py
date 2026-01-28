import os
import shutil

DOCUMENTS_DIR = os.path.join(os.path.expanduser("~"), "Documents")
MainFolder = os.path.join(DOCUMENTS_DIR, "BITS-EMS_Folder")

def CreateFolder(EmployeeId):
    EmployeeFolder = f"{EmployeeId}_File"
    path = os.path.join(MainFolder,EmployeeFolder)
    os.makedirs(path,exist_ok=True)
    return path

def _save_single_file(employee_folder, source_path, new_name):
    if not source_path:
        return None

    _, ext = os.path.splitext(source_path)
    new_filename = f"{new_name}{ext}"
    destination = os.path.join(employee_folder, new_filename)

    shutil.copy(source_path, destination)
    return destination

def SaveEmpFile(EmployeeId,files):
    employee_folder = CreateFolder(EmployeeId=EmployeeId)
    saved_paths = {}

    saved_paths["image"] = _save_single_file(employee_folder, files.get("image"), f"{EmployeeId}_image")
    saved_paths["cv"] = _save_single_file(employee_folder, files.get("cv"), f"{EmployeeId}_cv")
    saved_paths["certificate"] = _save_single_file(employee_folder, files.get("certificate"), f"{EmployeeId}_certificate")
    saved_paths["id"] = _save_single_file(employee_folder, files.get("id"), f"{EmployeeId}_id")
    saved_paths["contract"] = _save_single_file(employee_folder, files.get("contract"), f"{EmployeeId}_contract")

    return saved_paths