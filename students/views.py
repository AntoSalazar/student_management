from django.shortcuts import render, redirect
from django.contrib import messages

from .functional_core import (
    add_student, add_subject, update_grade, 
    remove_student, calculate_average, list_students
)
from .session_manager import StudentSessionManager


def home(request):
    """Main view showing student data and handling form submissions
    
    This view handles all operations for the student management system:
    - GET requests: Displays the management interface with student data
    - POST requests: Processes form submissions for various operations
    
    Args:
        request: The HTTP request object
    
    Returns:
        A rendered template or a redirect response
    """
    # Get the current state from the session using our session manager
    # This returns a lambda function that, when called, provides the current state
    state = StudentSessionManager.get_state(request.session)
    
    # Process any submitted forms (POST requests)
    if request.method == 'POST':
        # Extract the requested action from the form data
        action = request.POST.get('action')
        
        # Handle "add student" action
        if action == 'add_student':
            # Extract form data
            name = request.POST.get('name')
            subjects_str = request.POST.get('subjects')
            
            # Validate that required fields are provided
            if name and subjects_str:
                try:
                    # Parse the subjects string (format: "math:90, science:85")
                    subject_items = [item.strip() for item in subjects_str.split(',')]
                    subjects_dict = {}
                    
                    # Convert each item into a subject:grade pair
                    for item in subject_items:
                        if ':' in item:
                            subject, grade = item.split(':', 1)
                            subjects_dict[subject.strip()] = int(grade.strip())
                    
                    # Call the functional core to get a new state with the added student
                    new_state = add_student(state, name, subjects_dict)
                    
                    # Update the session with the new state
                    StudentSessionManager.update_session(request.session, new_state)
                    
                    # Add a success message
                    messages.success(request, f'Student {name} added successfully')
                except ValueError:
                    # Handle conversion errors (e.g., non-numeric grades)
                    messages.error(request, 'Error in subjects format. Use "subject:grade, subject2:grade2"')
            else:
                # Handle missing input fields
                messages.error(request, 'Please provide name and subjects')
        
        # Handle "add subject" action
        elif action == 'add_subject':
            # Extract form data
            name = request.POST.get('name')
            subject = request.POST.get('subject')
            grade = request.POST.get('grade')
            
            # Validate that required fields are provided
            if name and subject and grade:
                try:
                    # Convert grade to integer
                    grade = int(grade)
                    
                    # Call the functional core to get a new state with the added subject
                    new_state = add_subject(state, name, subject, grade)
                    
                    # Update the session with the new state
                    StudentSessionManager.update_session(request.session, new_state)
                    
                    # Add a success message
                    messages.success(request, f'Subject {subject} added to {name}')
                except ValueError:
                    # Handle conversion errors
                    messages.error(request, 'Grade must be a number')
            else:
                # Handle missing input fields
                messages.error(request, 'All fields are required')
        
        # Handle "update grade" action
        elif action == 'update_grade':
            # Extract form data
            name = request.POST.get('name')
            subject = request.POST.get('subject')
            grade = request.POST.get('grade')
            
            # Validate that required fields are provided
            if name and subject and grade:
                try:
                    # Convert grade to integer
                    grade = int(grade)
                    
                    # Call the functional core to get a new state with the updated grade
                    new_state = update_grade(state, name, subject, grade)
                    
                    # Update the session with the new state
                    StudentSessionManager.update_session(request.session, new_state)
                    
                    # Add a success message
                    messages.success(request, f'Grade updated for {name} in {subject}')
                except ValueError:
                    # Handle conversion errors
                    messages.error(request, 'Grade must be a number')
            else:
                # Handle missing input fields
                messages.error(request, 'All fields are required')
        
        # Handle "remove student" action
        elif action == 'remove_student':
            # Extract form data
            name = request.POST.get('name')
            
            # Validate that required fields are provided
            if name:
                # Call the functional core to get a new state without the student
                new_state = remove_student(state, name)
                
                # Update the session with the new state
                StudentSessionManager.update_session(request.session, new_state)
                
                # Add a success message
                messages.success(request, f'Student {name} removed successfully')
            else:
                # Handle missing input fields
                messages.error(request, 'Please provide the student name')
        
        # Handle "calculate average" action
        elif action == 'calculate_average':
            # Extract form data
            name = request.POST.get('name')
            
            # Validate that required fields are provided
            if name:
                # Check if the student exists
                if name in state():
                    # Call the functional core to calculate the average
                    avg_func = calculate_average(state, name)
                    
                    # Execute the returned lambda to get the average value
                    average = avg_func()
                    
                    # Add an info message with the result
                    messages.info(request, f'The average grade for {name} is: {average:.2f}')
                else:
                    # Handle non-existent student
                    messages.error(request, f'Student {name} not found')
            else:
                # Handle missing input fields
                messages.error(request, 'Please provide the student name')
        
        # Redirect to the same page to prevent form resubmission
        return redirect('home')
    
    # For GET requests, prepare data for the template
    student_data = state()
    
    # Get a formatted representation of all students and their grades
    students_list_func = list_students(state)
    students_formatted = students_list_func() if student_data else "No students registered"
    
    # Render the template with the prepared data
    return render(request, 'students/home.html', {
        'students': student_data,
        'students_formatted': students_formatted,
    })