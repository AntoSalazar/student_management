from django.shortcuts import render, redirect
from django.contrib import messages

from .functional_core import (
    add_student, add_subject, update_grade, 
    remove_student, calculate_average, list_students
)
from .session_manager import StudentSessionManager


def home(request):
    """Main view showing student data and form"""
    state = StudentSessionManager.get_state(request.session)
    
    # Process any submitted forms
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add_student':
            name = request.POST.get('name')
            subjects_str = request.POST.get('subjects')
            
            if name and subjects_str:
                try:
                    # Parse subjects_str (format: "math:90, science:85")
                    subject_items = [item.strip() for item in subjects_str.split(',')]
                    subjects_dict = {}
                    
                    for item in subject_items:
                        if ':' in item:
                            subject, grade = item.split(':', 1)
                            subjects_dict[subject.strip()] = int(grade.strip())
                    
                    new_state = add_student(state, name, subjects_dict)
                    StudentSessionManager.update_session(request.session, new_state)
                    messages.success(request, f'Student {name} added successfully')
                except ValueError:
                    messages.error(request, 'Error in subjects format. Use "subject:grade, subject2:grade2"')
            else:
                messages.error(request, 'Please provide name and subjects')
        
        elif action == 'add_subject':
            name = request.POST.get('name')
            subject = request.POST.get('subject')
            grade = request.POST.get('grade')
            
            if name and subject and grade:
                try:
                    grade = int(grade)
                    new_state = add_subject(state, name, subject, grade)
                    StudentSessionManager.update_session(request.session, new_state)
                    messages.success(request, f'Subject {subject} added to {name}')
                except ValueError:
                    messages.error(request, 'Grade must be a number')
            else:
                messages.error(request, 'All fields are required')
        
        elif action == 'update_grade':
            name = request.POST.get('name')
            subject = request.POST.get('subject')
            grade = request.POST.get('grade')
            
            if name and subject and grade:
                try:
                    grade = int(grade)
                    new_state = update_grade(state, name, subject, grade)
                    StudentSessionManager.update_session(request.session, new_state)
                    messages.success(request, f'Grade updated for {name} in {subject}')
                except ValueError:
                    messages.error(request, 'Grade must be a number')
            else:
                messages.error(request, 'All fields are required')
        
        elif action == 'remove_student':
            name = request.POST.get('name')
            
            if name:
                new_state = remove_student(state, name)
                StudentSessionManager.update_session(request.session, new_state)
                messages.success(request, f'Student {name} removed successfully')
            else:
                messages.error(request, 'Please provide the student name')
        
        elif action == 'calculate_average':
            name = request.POST.get('name')
            
            if name:
                if name in state():
                    avg_func = calculate_average(state, name)
                    average = avg_func()
                    messages.info(request, f'The average grade for {name} is: {average:.2f}')
                else:
                    messages.error(request, f'Student {name} not found')
            else:
                messages.error(request, 'Please provide the student name')
        
        return redirect('home')
    
    # Get data for the template
    student_data = state()
    students_list_func = list_students(state)
    students_formatted = students_list_func() if student_data else "No students registered"
    
    return render(request, 'students/home.html', {
        'students': student_data,
        'students_formatted': students_formatted,
    })