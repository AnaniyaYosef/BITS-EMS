# HR Employee Management System - Python Tkinter

A modern desktop application for managing employee records with a MySQL database backend.

## Features

- 🟢 **Green Sidebar** - Intuitive navigation menu
- 🔍 **Search** - Quick search employees by name or email
- 🎯 **Filter** - Filter by Name, Employee ID, or Department
- ➕ **Add** - Create new employee records
- ✏️ **Edit** - Double-click any employee to edit details
- 🗑️ **Delete** - Remove employee records
- 👁️ **View** - Display detailed employee information
- 💾 **MySQL Database** - All data persisted securely

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements_tkinter.txt
```

### 2. Ensure MySQL is Running
```bash
# MySQL should be running on localhost:3306
# Default credentials: root / Amoori.1927
# Database: bitsems
```

### 3. Run the Application
```bash
python hr_app.py
```

## Database Configuration

The app connects to:
- **Host**: localhost
- **Port**: 3306
- **User**: root
- **Password**: Amoori.1927
- **Database**: bitsems

The `employees` table is created automatically on first run with these columns:
- `employee_id` - AUTO_INCREMENT PRIMARY KEY
- `full_name` - VARCHAR(100)
- `department_name` - VARCHAR(100)
- `gender` - ENUM('Male', 'Female', 'Other')
- `email` - VARCHAR(100) UNIQUE
- `contact_number` - VARCHAR(20)
- `employment_date` - DATE

## File Structure

```
hr_app.py                  # Main application
requirements_tkinter.txt   # Python dependencies
SETUP_TKINTER.md          # Detailed setup guide
README.md                 # This file
```

## Troubleshooting

**Cannot connect to MySQL**
- Ensure MySQL service is running
- Check credentials are correct
- Verify database `bitsems` exists

**Email already exists**
- Each employee email must be unique
- Try a different email address

**Invalid date format**
- Use YYYY-MM-DD format for dates
- Example: 2024-01-15

## System Requirements

- Python 3.7+
- MySQL Server 5.7+
- Windows, macOS, or Linux

For detailed setup instructions, see [SETUP_TKINTER.md](SETUP_TKINTER.md)
