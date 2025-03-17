from django.contrib.sessions.backends.base import SessionBase

class StudentSessionManager:
    """Manages the student data in the Django session"""
    
    SESSION_KEY = 'student_data'
    
    @staticmethod
    def get_state(session):
        """Get the current state from the session"""
        if StudentSessionManager.SESSION_KEY not in session:
            session[StudentSessionManager.SESSION_KEY] = {}
        
        return lambda: session[StudentSessionManager.SESSION_KEY]
    
    @staticmethod
    def update_session(session, new_state_func):
        """Update the session with a new state"""
        session[StudentSessionManager.SESSION_KEY] = new_state_func()
        session.modified = True
        return lambda: session[StudentSessionManager.SESSION_KEY]