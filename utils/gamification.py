import math
from database import UserProfile

def calculate_level(xp: int) -> int:
    """
    Calculate level based on XP.
    Formula: Level = 1 + floor(sqrt(XP) / 10)
    
    Examples:
    - 0 XP -> Level 1
    - 99 XP -> Level 1
    - 100 XP -> Level 2
    - 400 XP -> Level 3
    - 900 XP -> Level 4
    """
    if xp < 0:
        return 1
    return 1 + int(math.sqrt(xp) / 10)

def process_xp_gain(session, user: UserProfile, amount: int) -> tuple[int, bool]:
    """
    Add XP to user and update level if necessary.
    
    Args:
        session: Database session
        user: UserProfile instance
        amount: Amount of XP to add
        
    Returns:
        tuple: (new_level, leveled_up_bool)
    """
    user.xp += amount
    
    new_level = calculate_level(user.xp)
    leveled_up = False
    
    if new_level > user.level:
        user.level = new_level
        leveled_up = True
    
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return user.level, leveled_up

def get_xp_for_level(level: int) -> int:
    """
    Calculate total XP required to reach a specific level.
    Inverse of Level = 1 + floor(sqrt(XP) / 10)
    sqrt(XP) / 10 = Level - 1
    sqrt(XP) = (Level - 1) * 10
    XP = ((Level - 1) * 10) ^ 2
    """
    if level <= 1:
        return 0
    return ((level - 1) * 10) ** 2

def get_level_progress(current_xp: int, current_level: int) -> dict:
    """
    Calculate progress towards the next level.
    
    Returns:
        dict: {
            'current_level_xp': XP required for current level (floor),
            'next_level_xp': XP required for next level (ceiling),
            'xp_in_level': XP gained within this level,
            'xp_needed_for_level': Total XP needed to go from current to next level,
            'percentage': Progress percentage (0.0 to 1.0)
        }
    """
    current_level_start_xp = get_xp_for_level(current_level)
    next_level_start_xp = get_xp_for_level(current_level + 1)
    
    xp_in_level = current_xp - current_level_start_xp
    xp_needed_for_level = next_level_start_xp - current_level_start_xp
    
    if xp_needed_for_level <= 0:
        percentage = 1.0
    else:
        percentage = min(1.0, max(0.0, xp_in_level / xp_needed_for_level))
        
    return {
        'current_level_xp': current_level_start_xp,
        'next_level_xp': next_level_start_xp,
        'xp_in_level': xp_in_level,
        'xp_needed_for_level': xp_needed_for_level,
        'percentage': percentage
    }
