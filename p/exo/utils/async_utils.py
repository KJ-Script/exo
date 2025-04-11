"""
Async utility functions.
"""
import asyncio
from typing import Any, Callable, List
from functools import wraps

def async_retry(max_retries: int = 3, delay: float = 1.0):
    """
    Decorator for retrying async functions.
    
    Args:
        max_retries: Maximum number of retry attempts
        delay: Delay between retries in seconds
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        await asyncio.sleep(delay)
            raise last_exception
        return wrapper
    return decorator

async def gather_with_concurrency(n: int, *tasks: List[Callable]) -> List[Any]:
    """
    Run multiple tasks with a concurrency limit.
    
    Args:
        n: Maximum number of concurrent tasks
        tasks: List of coroutines to run
        
    Returns:
        List of results from the tasks
    """
    semaphore = asyncio.Semaphore(n)
    
    async def sem_task(task):
        async with semaphore:
            return await task
    
    return await asyncio.gather(*(sem_task(task) for task in tasks)) 