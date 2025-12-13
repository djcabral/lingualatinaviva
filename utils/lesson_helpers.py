"""
Helper utility to extract lesson data safely from SQLAlchemy objects.
Prevents DetachedInstanceError by extracting all needed attributes within session.
"""

def extract_lesson_data(lesson):
    """
    Extract lesson attributes into a plain dict to avoid DetachedInstanceError.
    
    Args:
        lesson: SQLAlchemy Lesson object (must be called within session context)
        
    Returns:
        dict with lesson data
    """
    if lesson is None:
        return None
        
    return {
        'id': lesson.id,
        'lesson_number': lesson.lesson_number,
        'title': lesson.title,
        'content_markdown': lesson.content_markdown if hasattr(lesson, 'content_markdown') else None,
    }
