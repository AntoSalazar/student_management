from django.contrib.sessions.backends.base import SessionBase

class StudentSessionManager:
    """Manages the student data in the Django session
    
    This class serves as a bridge between the functional programming paradigm
    and Django's session management system. It provides methods to retrieve
    and update state in a way that's compatible with our functional core.
    """
    
    # Key used to store student data in the Django session
    SESSION_KEY = 'student_data'
    
    @staticmethod
    def get_state(session):
        """Get the current state from the session
        
        This method retrieves the current state from the Django session.
        If no state exists yet, it initializes an empty dictionary.
        
        Args:
            session: The Django session object
        
        Returns:
            A lambda function that, when called, returns the current state
        """
        # Check if our session key exists
        if StudentSessionManager.SESSION_KEY not in session:
            # If not, initialize an empty dictionary
            session[StudentSessionManager.SESSION_KEY] = {}
        
        # Return a lambda function that gives access to the session data
        # This maintains compatibility with our functional core
        return lambda: session[StudentSessionManager.SESSION_KEY]
    
    @staticmethod
    def update_session(session, new_state_func):
        """Update the session with a new state
        
        This method updates the Django session with a new state produced
        by one of our functional operations.
        
        Args:
            session: The Django session object
            new_state_func: A lambda function that returns the new state
        
        Returns:
            A lambda function that, when called, returns the updated state
        """
        # Execute the lambda function to get the new state
        session[StudentSessionManager.SESSION_KEY] = new_state_func()
        
        # Mark the session as modified so Django saves it
        session.modified = True
        
        # Return a lambda function that gives access to the updated session data
        return lambda: session[StudentSessionManager.SESSION_KEY]