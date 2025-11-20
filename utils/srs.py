from datetime import datetime, timedelta
from database.models import ReviewLog

def calculate_next_review(quality: int, previous_review: ReviewLog = None) -> dict:
    """
    Implement SM-2 Algorithm.
    Returns dict with new ease_factor, interval, repetitions.
    """
    if previous_review:
        ease_factor = previous_review.ease_factor
        interval = previous_review.interval
        repetitions = previous_review.repetitions
    else:
        ease_factor = 2.5
        interval = 0
        repetitions = 0

    if quality >= 3:
        if repetitions == 0:
            interval = 1
        elif repetitions == 1:
            interval = 6
        else:
            interval = int(interval * ease_factor)
        
        repetitions += 1
        ease_factor = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    else:
        repetitions = 0
        interval = 1
    
    if ease_factor < 1.3:
        ease_factor = 1.3
        
    return {
        "ease_factor": ease_factor,
        "interval": interval,
        "repetitions": repetitions,
        "next_review_date": datetime.utcnow() + timedelta(days=interval)
    }
