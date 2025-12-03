"""
Prometheus Metrics Exporter.

Defines and exposes application metrics for monitoring.
"""
from prometheus_client import Counter, Histogram, Gauge
import time

# Request Metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["method", "endpoint"]
)

# LLM Metrics
LLM_REQUEST_COUNT = Counter(
    "llm_requests_total",
    "Total LLM API calls",
    ["provider", "model"]
)

LLM_TOKEN_USAGE = Counter(
    "llm_token_usage_total",
    "Total LLM tokens used",
    ["provider", "model", "type"] # type: prompt, completion
)

LLM_LATENCY = Histogram(
    "llm_request_duration_seconds",
    "LLM API latency",
    ["provider", "model"]
)

# SQL Metrics
SQL_QUERY_COUNT = Counter(
    "sql_queries_total",
    "Total SQL queries executed",
    ["status"] # success, failed
)

SQL_EXECUTION_TIME = Histogram(
    "sql_execution_duration_seconds",
    "SQL query execution time"
)

def track_time(histogram: Histogram, labels: dict = None):
    """Decorator to track execution time."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                duration = time.time() - start_time
                if labels:
                    histogram.labels(**labels).observe(duration)
                else:
                    histogram.observe(duration)
        return wrapper
    return decorator
