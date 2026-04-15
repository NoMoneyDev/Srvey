"""
Request/Response logging middleware for FastAPI.
Tracks all HTTP requests and responses with timing information.
"""

import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from logger import log_request, log_response, log_error


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log all HTTP requests and responses."""

    async def dispatch(self, request: Request, call_next) -> Response:
        # Generate unique request ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        # Extract user info if available
        user_id = None
        auth_header = request.headers.get("authorization", "")
        if auth_header.startswith("Bearer "):
            # Could parse JWT here to get actual user_id
            user_id = "authenticated"

        # Log incoming request
        endpoint = f"{request.url.path}"
        log_request(request.method, endpoint, user_id, request_id)

        # Measure response time
        start_time = time.time()

        try:
            response = await call_next(request)
        except Exception as exc:
            # Log error
            log_error(exc, endpoint, user_id)
            raise

        # Calculate response time
        response_time_ms = (time.time() - start_time) * 1000

        # Log response
        log_response(
            request.method,
            endpoint,
            response.status_code,
            response_time_ms,
            user_id,
            request_id,
        )

        # Add request ID to response headers for tracing
        response.headers["X-Request-ID"] = request_id

        return response
