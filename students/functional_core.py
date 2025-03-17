from functools import reduce


def add_student(students, name, subjects_grades):
    """Adds a new student with their subjects and grades"""
    return lambda: {**students(), name: subjects_grades}


def add_subject(students, name, subject, grade):
    """Adds a new subject to an existing student"""
    if name not in students():
        return students
    
    updated_subjects = {**students()[name], subject: grade}
    return lambda: {**students(), name: updated_subjects}


def update_grade(students, name, subject, new_grade):
    """Updates the grade for a specific subject"""
    if name not in students() or subject not in students()[name]:
        return students
    
    updated_subjects = {**students()[name], subject: new_grade}
    return lambda: {**students(), name: updated_subjects}


def remove_student(students, name):
    """Removes a student from the dictionary"""
    return lambda: {k: v for k, v in students().items() if k != name}


def calculate_average(students, name):
    """Calculates the average grade for a student"""
    if name not in students():
        return lambda: 0
    
    grades = list(students()[name].values())
    if not grades:
        return lambda: 0
    
    return lambda: reduce(lambda acc, x: acc + x, grades, 0) / len(grades)


def list_students(students):
    """Returns a formatted string with all students and their grades"""
    result = []
    for name, subjects in students().items():
        subjects_str = ", ".join([f"{subject}: {grade}" for subject, grade in subjects.items()])
        result.append(f"{name}: {subjects_str}")
    
    return lambda: "\n".join(result)


# Initial empty state
def initial_state():
    return lambda: {}