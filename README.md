# Student Management System

A Django implementation of a student management system using functional programming principles. This application allows you to manage student information, subjects, and grades without using a persistent database.

## Features

- Add new students with their subjects and grades
- Add new subjects to existing students
- Update grades for existing subjects
- Remove students from the system
- Calculate the average grade for a student
- List all students with their subjects and grades

## Technology Stack

- Python 3.x
- Django 5.x
- Functional Programming approach

## Architecture

The application follows a functional programming paradigm within the Django framework:

- **Functional Core**: Pure functions that handle data transformations
- **Session Management**: Bridges functional programming with Django sessions
- **Web Interface**: Forms and displays to interact with the system

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/AntoSalazar/student_management.git
   cd student_management
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For bash/zsh
   # OR
   source venv/bin/activate.fish  # For fish shell
   ```

3. Install Django:
   ```bash
   pip install django
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

6. Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Project Structure

- `functional_core.py`: Contains the pure functional operations
- `session_manager.py`: Manages state through Django sessions
- `views.py`: Handles HTTP requests and form submissions
- `urls.py`: Defines URL routing
- `templates/students/home.html`: The user interface

## Usage

### Adding a Student

Enter the student's name and their subjects with grades in the format:
```
mathematics:85, history:90, science:78
```

### Adding a Subject

Select an existing student and provide the subject name and grade.

### Updating a Grade

Select a student and subject, then enter the new grade.

### Removing a Student

Enter the name of the student to remove them from the system.

### Calculating Average

Enter a student's name to calculate their average grade across all subjects.

### Listing Students

View all students with their subjects and grades.

## Data Persistence

This application intentionally doesn't use a database for storing student information. All data is stored in the Django session and will be lost when the session expires. This design aligns with the functional programming principles of the original implementation.

