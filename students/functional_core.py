from functools import reduce  


# Function to add a new student to the students dictionary
def add_student(students, name, subjects_grades):
    """Adds a new student with their subjects and grades
    Returns:
        A lambda function that, when called, returns a new dictionary with the added student
    """
    # Create a new dictionary with all existing students plus the new one
    # The ** operator unpacks the existing students dictionary
    # We then add a new key-value pair with the student name and their subjects/grades
    return lambda: {**students(), name: subjects_grades}


# Function to add a new subject to an existing student
def add_subject(students, name, subject, grade):
    """Adds a new subject to an existing student
    Returns:
        A lambda function that, when called, returns an updated dictionary
    """
    # Check if the student exists in the dictionary
    if name not in students():
        # If not, return the original state unchanged
        return students
    
    # Create a new dictionary for the student's subjects by:
    # 1. Unpacking their existing subjects with **
    # 2. Adding the new subject:grade pair
    updated_subjects = {**students()[name], subject: grade}
    
    # Return a lambda that creates a new dictionary with all students
    # but with the specified student's subjects updated
    return lambda: {**students(), name: updated_subjects}


# Function to update a grade for an existing subject
def update_grade(students, name, subject, new_grade):
    """Updates the grade for a specific subject
    Returns:
        A lambda function that, when called, returns an updated dictionary
    """
    # Check if the student exists and has the specified subject
    if name not in students() or subject not in students()[name]:
        # If either condition is not met, return the original state unchanged
        return students
    
    # Create a new dictionary of subjects with the updated grade
    # This preserves immutability by not modifying the original dictionary
    updated_subjects = {**students()[name], subject: new_grade}
    
    # Return a lambda that builds a new complete state with the update
    return lambda: {**students(), name: updated_subjects}


# Function to remove a student from the dictionary
def remove_student(students, name):
    """Removes a student from the dictionary
    Returns:
        A lambda function that, when called, returns a dictionary without the specified student
    """
    # Use dictionary comprehension to create a new dictionary
    # that includes all key-value pairs except for the specified student
    return lambda: {k: v for k, v in students().items() if k != name}


# Function to calculate the average grade for a student
def calculate_average(students, name):
    """Calculates the average grade for a student
    Returns:
        A lambda function that, when called, returns the average grade as a float
    """
    # Check if the student exists in the dictionary
    if name not in students():
        # If not, return zero as the average
        return lambda: 0
    
    # Get all grades for the student as a list
    grades = list(students()[name].values())
    
    # Check if the student has any grades
    if not grades:
        # If no grades, return zero as the average
        return lambda: 0
    
    # Calculate the average using the reduce function:
    # 1. Start with initial value 0 (third parameter of reduce)
    # 2. For each grade (x), add it to the accumulator (acc)
    # 3. Divide the sum by the number of grades
    return lambda: reduce(lambda acc, x: acc + x, grades, 0) / len(grades)


# Function to generate a formatted string listing all students and their grades
def list_students(students):
    """Returns a formatted string with all students and their grades
    Returns:
        A lambda function that, when called, returns a formatted string
    """
    # Initialize an empty list to store the formatted strings
    result = []
    
    # Iterate through each student and their subjects
    for name, subjects in students().items():
        # Create a comma-separated string of "subject: grade" pairs
        # using list comprehension and string formatting
        subjects_str = ", ".join([f"{subject}: {grade}" for subject, grade in subjects.items()])
        
        # Add a formatted line for this student to the results list
        result.append(f"{name}: {subjects_str}")
    
    # Return a lambda that joins all the lines with newlines when called
    return lambda: "\n".join(result)


# Function to provide an initial empty state
def initial_state():
    """Creates an initial empty state for the application
    
    Returns:
        A lambda function that returns an empty dictionary
    """
    # Return a lambda that gives an empty dictionary
    # This serves as the starting point for the application
    return lambda: {}