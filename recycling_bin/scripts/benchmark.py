"""
Performance benchmarking script.
"""
import time
import functools
from typing import Callable, Any

def benchmark(func: Callable) -> Callable:
    """
    Decorator to benchmark function execution time.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        print(f"{func.__name__} executed in {execution_time:.4f} seconds")
        return result
    return wrapper

def benchmark_with_stats(func: Callable) -> Callable:
    """
    Decorator to benchmark function with detailed statistics.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        times = []
        for _ in range(10):  # Run 10 times for average
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            times.append(end_time - start_time)
        
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        print(f"{func.__name__} performance statistics:")
        print(f"  Average: {avg_time:.4f} seconds")
        print(f"  Minimum: {min_time:.4f} seconds")
        print(f"  Maximum: {max_time:.4f} seconds")
        print(f"  Total runs: {len(times)}")
        
        return result
    return wrapper

if __name__ == "__main__":
    # Example usage
    @benchmark
    def example_function():
        time.sleep(0.1)  # Simulate some work
        return "Done"
    
    result = example_function()
    print(f"Result: {result}")