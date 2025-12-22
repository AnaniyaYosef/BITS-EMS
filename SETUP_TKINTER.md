# HR Employee Management System - Python Tkinter Edition

## Prerequisites

1. **Python 3.7+** installed on your machine
2. **MySQL Server** running on localhost:3306
3. **Database**: `bitsems` must exist

## Installation Steps

### Step 1: Install Python Dependencies

```bash
pip install -r requirements_tkinter.txt
```

Or install manually:
```bash
pip install mysql-connector-python
```

### Step 2: Ensure MySQL is Running

Make sure your MySQL server is running:
```bash
# On Windows (if installed with MySQL Service)
# It should be running automatically

# On Mac
brew services start mysql

# On Linux
sudo service mysql start
```

### Step 3: Create the Database

Connect to MySQL and create the database:
```bash
mysql -u root -p
# Enter password: Amoori.1927

CREATE DATABASE IF NOT EXISTS bitsems;
USE bitsems;
```

### Step 4: Run the Application

```bash
python hr_app.py
```

## Features

- ✅ **Search Employees** - Search by name or email
- ✅ **Filter** - Filter by Name, Employee ID, or Department
- ✅ **Add Employee** - Create new employee records
- ✅ **Edit Employee** - Double-click any employee row to edit
- ✅ **Delete Employee** - Remove employee records
- ✅ **View Employee** - View detailed employee information
- ✅ **MySQL Integration** - All data persisted in your database

## Database Schema

The application automatically creates the `employees` table with:
- `employee_id` - AUTO_INCREMENT PRIMARY KEY
- `full_name` - VARCHAR(100)
- `department_name` - VARCHAR(100)
- `gender` - ENUM('Male', 'Female', 'Other')
- `email` - VARCHAR(100) UNIQUE
- `contact_number` - VARCHAR(20)
- `employment_date` - DATE

## Connection Details

- **Host**: localhost
- **Port**: 3306
- **User**: root
- **Password**: Amoori.1927
- **Database**: bitsems

## Troubleshooting

### "Cannot connect to database"
- Ensure MySQL server is running
- Check that your username, password, and database name are correct
- Verify the database `bitsems` exists

### "Column 'email' is not unique"
- An employee with that email already exists in the database
- Use a different email address

### "Invalid date format"
- Use YYYY-MM-DD format for employment dates
- Example: 2024-01-15

## UI Overview

### Sidebar (Green)
Quick access buttons for common operations:
- Add Employee
- Edit Employee
- Delete Employee
- Search Employee
- View Employee
- Leave Request Form

### Main Content Area
- **Search Bar** - Quick search by name/email
- **Filters** - Filter by Name, Employee ID, Department
- **Table** - Display all employees with full details
