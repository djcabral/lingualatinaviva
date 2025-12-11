"""
Improved Utilities for Error Handling, Validation, and Monitoring

Provides reusable components for:
- Enhanced error handling with context
- Input validation with Pydantic
- Performance monitoring and metrics
- Circuit breaker pattern
- Retry logic with exponential backoff
"""

import functools
import logging
import threading
import time
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, List, Optional, Type, TypeVar

from pydantic import BaseModel, Field, ValidationError, validator

logger = logging.getLogger(__name__)

T = TypeVar("T")
E = TypeVar("E", bound=Exception)


# ============================================================================
# ERROR HANDLING
# ============================================================================


class ErrorSeverity(str, Enum):
    """Error severity levels"""

    CRITICAL = "critical"  # System cannot continue
    ERROR = "error"  # Operation failed
    WARNING = "warning"  # Operation degraded
    INFO = "info"  # Informational


class ApplicationError(Exception):
    """Base application error with context"""

    def __init__(
        self,
        message: str,
        severity: ErrorSeverity = ErrorSeverity.ERROR,
        context: dict = None,
        cause: Exception = None,
    ):
        self.message = message
        self.severity = severity
        self.context = context or {}
        self.cause = cause
        self.timestamp = datetime.utcnow()
        super().__init__(self.message)

    def to_dict(self) -> dict:
        """Convert to dictionary for logging/serialization"""
        return {
            "type": self.__class__.__name__,
            "message": self.message,
            "severity": self.severity.value,
            "context": self.context,
            "timestamp": self.timestamp.isoformat(),
            "cause": str(self.cause) if self.cause else None,
        }

    def __str__(self) -> str:
        ctx_str = " | ".join(f"{k}={v}" for k, v in self.context.items())
        base = f"[{self.severity.upper()}] {self.message}"
        return f"{base} | {ctx_str}" if ctx_str else base


class ValidationError(ApplicationError):
    """Input validation error"""

    def __init__(self, message: str, field: str = None, context: dict = None):
        ctx = context or {}
        if field:
            ctx["field"] = field
        super().__init__(message, ErrorSeverity.WARNING, ctx)


class DatabaseError(ApplicationError):
    """Database operation error"""

    def __init__(self, message: str, context: dict = None):
        super().__init__(message, ErrorSeverity.ERROR, context)


class ExternalServiceError(ApplicationError):
    """External service call failed"""

    def __init__(self, service: str, message: str, context: dict = None):
        ctx = context or {}
        ctx["service"] = service
        super().__init__(message, ErrorSeverity.WARNING, ctx)


class RetryableError(ApplicationError):
    """Error that may succeed if retried"""

    def __init__(self, message: str, retry_after_seconds: int = 1):
        ctx = {"retry_after_seconds": retry_after_seconds}
        super().__init__(message, ErrorSeverity.INFO, ctx)


def handle_exception(
    exception: Exception,
    operation: str,
    logger_instance: logging.Logger = None,
) -> None:
    """
    Handle exception with context logging.

    Args:
        exception: The exception that occurred
        operation: Name of the operation that failed
        logger_instance: Logger to use (uses default if None)
    """
    log = logger_instance or logger

    if isinstance(exception, ApplicationError):
        if exception.severity in [ErrorSeverity.CRITICAL, ErrorSeverity.ERROR]:
            log.error(
                f"Operation '{operation}' failed: {exception}",
                extra={"error_dict": exception.to_dict()},
                exc_info=True,
            )
        else:
            log.warning(f"Operation '{operation}' warning: {exception}")
    else:
        log.error(
            f"Unexpected error in '{operation}': {exception}",
            exc_info=True,
        )


# ============================================================================
# VALIDATION
# ============================================================================


class ValidatedRequest(BaseModel):
    """Base class for validated requests"""

    class Config:
        validate_assignment = True


class SearchRequest(ValidatedRequest):
    """Validated search request"""

    query: str = Field(..., min_length=1, max_length=100)
    limit: int = Field(default=50, ge=1, le=500)
    offset: int = Field(default=0, ge=0)

    @validator("query")
    def query_must_be_clean(cls, v):
        """Sanitize query"""
        return v.strip().lower()


class PaginationParams(ValidatedRequest):
    """Validated pagination parameters"""

    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=50, ge=1, le=500)

    @property
    def offset(self) -> int:
        """Calculate offset from page"""
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        """Get limit"""
        return self.page_size


def validate_input(validation_class: Type[T]) -> Callable:
    """
    Decorator to validate function input against Pydantic model.

    Args:
        validation_class: Pydantic model class to validate against

    Returns:
        Decorator function

    Example:
        >>> @validate_input(SearchRequest)
        ... def search(req: SearchRequest):
        ...     return search_implementation(req)
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # Get the validated object (first positional arg or from kwargs)
                if args:
                    validated_obj = validation_class(**args[0].__dict__)
                    args = (validated_obj,) + args[1:]
                else:
                    validated_obj = validation_class(**kwargs)

                return func(*args, **kwargs)
            except ValidationError as e:
                raise ValidationError(
                    f"Input validation failed: {e}",
                    context={"validation_errors": e.errors()},
                )

        return wrapper

    return decorator


# ============================================================================
# RETRY LOGIC
# ============================================================================


class RetryConfig:
    """Configuration for retry behavior"""

    def __init__(
        self,
        max_attempts: int = 3,
        initial_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        jitter: bool = True,
    ):
        self.max_attempts = max_attempts
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter

    def get_delay(self, attempt: int) -> float:
        """Calculate delay for given attempt number"""
        delay = min(
            self.initial_delay * (self.exponential_base ** (attempt - 1)),
            self.max_delay,
        )

        if self.jitter:
            import random

            delay *= 0.5 + random.random()  # Add randomness

        return delay


def retry(
    config: RetryConfig = None,
    retryable_exceptions: tuple = (Exception,),
    on_retry: Callable = None,
) -> Callable:
    """
    Decorator to retry function with exponential backoff.

    Args:
        config: RetryConfig instance (uses defaults if None)
        retryable_exceptions: Tuple of exceptions that trigger retry
        on_retry: Callback function called on each retry

    Returns:
        Decorator function

    Example:
        >>> @retry(retryable_exceptions=(ConnectionError,))
        ... def connect_to_db():
        ...     return database.connect()
    """
    if config is None:
        config = RetryConfig()

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(1, config.max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except retryable_exceptions as e:
                    last_exception = e

                    if attempt < config.max_attempts:
                        delay = config.get_delay(attempt)
                        logger.warning(
                            f"Attempt {attempt} failed: {e}. "
                            f"Retrying in {delay:.2f}s..."
                        )

                        if on_retry:
                            on_retry(attempt, delay, e)

                        time.sleep(delay)
                    else:
                        logger.error(f"All {config.max_attempts} attempts failed")

            raise last_exception or Exception("Unknown retry failure")

        return wrapper

    return decorator


# ============================================================================
# CIRCUIT BREAKER
# ============================================================================


class CircuitState(str, Enum):
    """Circuit breaker states"""

    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if recovered


class CircuitBreaker:
    """
    Circuit breaker pattern implementation.

    Prevents cascading failures by stopping requests to failing services.
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        success_threshold: int = 2,
        timeout_seconds: int = 60,
    ):
        self.failure_threshold = failure_threshold
        self.success_threshold = success_threshold
        self.timeout_seconds = timeout_seconds

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: Optional[datetime] = None
        self._lock = threading.RLock()

    def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute function with circuit breaker protection.

        Args:
            func: Function to execute
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Function result

        Raises:
            CircuitBreakerOpen: If circuit is open
        """
        with self._lock:
            self._check_timeout()

            if self.state == CircuitState.OPEN:
                raise CircuitBreakerOpen(
                    "Circuit breaker is OPEN - service unavailable"
                )

            try:
                result = func(*args, **kwargs)
                self._on_success()
                return result
            except Exception as e:
                self._on_failure()
                raise

    def _check_timeout(self) -> None:
        """Check if timeout has elapsed to transition to HALF_OPEN"""
        if self.state == CircuitState.OPEN:
            if self.last_failure_time:
                elapsed = (datetime.utcnow() - self.last_failure_time).total_seconds()
                if elapsed >= self.timeout_seconds:
                    logger.info("Circuit breaker transitioning to HALF_OPEN")
                    self.state = CircuitState.HALF_OPEN
                    self.success_count = 0

    def _on_success(self) -> None:
        """Handle successful call"""
        self.failure_count = 0

        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                logger.info("Circuit breaker CLOSED (recovered)")
                self.state = CircuitState.CLOSED

    def _on_failure(self) -> None:
        """Handle failed call"""
        self.failure_count += 1
        self.last_failure_time = datetime.utcnow()

        if self.failure_count >= self.failure_threshold:
            if self.state != CircuitState.OPEN:
                logger.error(
                    f"Circuit breaker OPEN (failed {self.failure_count} times)"
                )
            self.state = CircuitState.OPEN

    def get_state(self) -> str:
        """Get current circuit state"""
        with self._lock:
            self._check_timeout()
            return self.state.value


class CircuitBreakerOpen(Exception):
    """Exception raised when circuit breaker is open"""

    pass


def circuit_breaker(
    failure_threshold: int = 5,
    success_threshold: int = 2,
    timeout_seconds: int = 60,
) -> Callable:
    """
    Decorator for circuit breaker pattern.

    Args:
        failure_threshold: Number of failures before opening
        success_threshold: Number of successes to close (HALF_OPEN)
        timeout_seconds: Time before retrying (HALF_OPEN)

    Returns:
        Decorator function

    Example:
        >>> @circuit_breaker(failure_threshold=5, timeout_seconds=30)
        ... def call_external_api():
        ...     return requests.get('http://api.example.com')
    """
    breaker = CircuitBreaker(
        failure_threshold=failure_threshold,
        success_threshold=success_threshold,
        timeout_seconds=timeout_seconds,
    )

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return breaker.call(func, *args, **kwargs)

        wrapper._circuit_breaker = breaker  # Expose for inspection
        return wrapper

    return decorator


# ============================================================================
# PERFORMANCE MONITORING
# ============================================================================


class PerformanceMetrics:
    """Track performance metrics"""

    def __init__(self, name: str):
        self.name = name
        self.call_count = 0
        self.total_time_ms = 0.0
        self.min_time_ms = float("inf")
        self.max_time_ms = 0.0
        self.error_count = 0
        self._lock = threading.Lock()

    def record(self, duration_ms: float, error: bool = False) -> None:
        """Record metric"""
        with self._lock:
            self.call_count += 1
            self.total_time_ms += duration_ms
            self.min_time_ms = min(self.min_time_ms, duration_ms)
            self.max_time_ms = max(self.max_time_ms, duration_ms)
            if error:
                self.error_count += 1

    @property
    def avg_time_ms(self) -> float:
        """Average execution time"""
        if self.call_count == 0:
            return 0.0
        return self.total_time_ms / self.call_count

    @property
    def error_rate(self) -> float:
        """Error rate as percentage"""
        if self.call_count == 0:
            return 0.0
        return (self.error_count / self.call_count) * 100

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "call_count": self.call_count,
            "avg_time_ms": round(self.avg_time_ms, 2),
            "min_time_ms": round(self.min_time_ms, 2)
            if self.min_time_ms != float("inf")
            else None,
            "max_time_ms": round(self.max_time_ms, 2),
            "error_count": self.error_count,
            "error_rate_percent": round(self.error_rate, 2),
        }

    def reset(self) -> None:
        """Reset metrics"""
        with self._lock:
            self.call_count = 0
            self.total_time_ms = 0.0
            self.min_time_ms = float("inf")
            self.max_time_ms = 0.0
            self.error_count = 0


class MetricsRegistry:
    """Registry of performance metrics"""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.metrics = {}
        return cls._instance

    def get_or_create(self, name: str) -> PerformanceMetrics:
        """Get or create metrics for a name"""
        if name not in self.metrics:
            self.metrics[name] = PerformanceMetrics(name)
        return self.metrics[name]

    def get_all(self) -> dict:
        """Get all metrics"""
        return {name: m.to_dict() for name, m in self.metrics.items()}

    def reset_all(self) -> None:
        """Reset all metrics"""
        for m in self.metrics.values():
            m.reset()


def monitor_performance(name: str = None) -> Callable:
    """
    Decorator to monitor function performance.

    Args:
        name: Name for metrics (uses function name if None)

    Returns:
        Decorator function

    Example:
        >>> @monitor_performance()
        ... def expensive_operation():
        ...     return compute_something()

        >>> # Later, get metrics
        >>> metrics = MetricsRegistry().get_all()
    """

    def decorator(func: Callable) -> Callable:
        metric_name = name or func.__qualname__
        registry = MetricsRegistry()

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            metrics = registry.get_or_create(metric_name)
            start = time.time()

            try:
                result = func(*args, **kwargs)
                duration_ms = (time.time() - start) * 1000
                metrics.record(duration_ms, error=False)
                return result
            except Exception as e:
                duration_ms = (time.time() - start) * 1000
                metrics.record(duration_ms, error=True)
                raise

        return wrapper

    return decorator


# ============================================================================
# CACHING WITH TTL
# ============================================================================


class CachedValue:
    """Cache entry with TTL"""

    def __init__(self, value: Any, ttl_seconds: int):
        self.value = value
        self.created_at = time.time()
        self.ttl_seconds = ttl_seconds

    def is_expired(self) -> bool:
        """Check if expired"""
        return (time.time() - self.created_at) > self.ttl_seconds


class TTLCache:
    """Simple TTL-based cache"""

    def __init__(self, ttl_seconds: int = 300, max_size: int = 1000):
        self.ttl_seconds = ttl_seconds
        self.max_size = max_size
        self.cache = {}
        self._lock = threading.RLock()

    def get(self, key: str) -> Optional[Any]:
        """Get from cache"""
        with self._lock:
            if key not in self.cache:
                return None

            entry = self.cache[key]
            if entry.is_expired():
                del self.cache[key]
                return None

            return entry.value

    def set(self, key: str, value: Any, ttl_seconds: int = None) -> None:
        """Set cache value"""
        with self._lock:
            ttl = ttl_seconds or self.ttl_seconds
            self.cache[key] = CachedValue(value, ttl)

            # Evict oldest if size exceeded
            if len(self.cache) > self.max_size:
                oldest_key = min(
                    self.cache.keys(), key=lambda k: self.cache[k].created_at
                )
                del self.cache[oldest_key]

    def clear(self) -> None:
        """Clear cache"""
        with self._lock:
            self.cache.clear()

    def cleanup_expired(self) -> int:
        """Remove expired entries"""
        with self._lock:
            expired = [k for k, v in self.cache.items() if v.is_expired()]
            for k in expired:
                del self.cache[k]
            return len(expired)

    def get_stats(self) -> dict:
        """Get cache statistics"""
        with self._lock:
            return {
                "size": len(self.cache),
                "max_size": self.max_size,
                "ttl_seconds": self.ttl_seconds,
            }


def cached(ttl_seconds: int = 300, key_fn: Callable = None) -> Callable:
    """
    Decorator to cache function result with TTL.

    Args:
        ttl_seconds: Time to live in seconds
        key_fn: Custom function to generate cache key (uses args/kwargs if None)

    Returns:
        Decorator function

    Example:
        >>> @cached(ttl_seconds=300)
        ... def expensive_computation(x, y):
        ...     return x + y
    """
    cache = TTLCache(ttl_seconds=ttl_seconds)

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            if key_fn:
                cache_key = key_fn(*args, **kwargs)
            else:
                cache_key = f"{func.__qualname__}:{str(args)}:{str(kwargs)}"

            # Try cache
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                logger.debug(f"Cache hit for {cache_key}")
                return cached_value

            # Execute function
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl_seconds)
            return result

        wrapper._cache = cache  # Expose cache for inspection
        return wrapper

    return decorator


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    # Errors
    "ErrorSeverity",
    "ApplicationError",
    "ValidationError",
    "DatabaseError",
    "ExternalServiceError",
    "RetryableError",
    "handle_exception",
    # Validation
    "ValidatedRequest",
    "SearchRequest",
    "PaginationParams",
    "validate_input",
    # Retry
    "RetryConfig",
    "retry",
    # Circuit Breaker
    "CircuitState",
    "CircuitBreaker",
    "CircuitBreakerOpen",
    "circuit_breaker",
    # Monitoring
    "PerformanceMetrics",
    "MetricsRegistry",
    "monitor_performance",
    # Caching
    "TTLCache",
    "cached",
]
