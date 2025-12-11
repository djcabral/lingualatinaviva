"""
Simple caching utility for performance optimization.
"""
import functools
import time
from typing import Any, Callable

# Simple in-memory cache
_cache = {}
_cache_ttl = {}

def cached(ttl: int = 300):
    """
    Decorator for caching function results.
    
    Args:
        ttl: Time to live in seconds (default: 5 minutes)
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create a cache key based on function name and arguments
            key = f"{func.__name__}:{hash(str(args) + str(sorted(kwargs.items())))}"
            
            # Check if we have a cached result that hasn't expired
            if key in _cache:
                result, timestamp = _cache[key]
                if time.time() - timestamp < ttl:
                    return result
            
            # Call the function and cache the result
            result = func(*args, **kwargs)
            _cache[key] = (result, time.time())
            
            # Clean up expired entries periodically
            _cleanup_expired(ttl)
            
            return result
        return wrapper
    return decorator

def _cleanup_expired(ttl: int):
    """Clean up expired cache entries."""
    current_time = time.time()
    expired_keys = [
        key for key, (_, timestamp) in _cache.items()
        if current_time - timestamp >= ttl
    ]
    for key in expired_keys:
        del _cache[key]

def clear_cache():
    """Clear all cached entries."""
    global _cache
    _cache = {}