"""
HTTP Cache headers utilities for optimized browser caching
"""
from functools import wraps
from flask import make_response


def cache_control(max_age=300, public=True, immutable=False):
    """
    Add Cache-Control headers to response for browser caching

    Args:
        max_age: Time in seconds to cache (default 5 minutes)
        public: Allow CDN/proxy caching (default True)
        immutable: Mark resource as never changing (for match data)
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            response = make_response(f(*args, **kwargs))

            # Build Cache-Control directive
            directives = []
            directives.append('public' if public else 'private')
            directives.append(f'max-age={max_age}')

            if immutable:
                directives.append('immutable')

            response.headers['Cache-Control'] = ', '.join(directives)

            # Add ETag for validation
            # Flask will auto-generate ETag if not set

            return response
        return decorated_function
    return decorator


def no_cache():
    """Disable all caching (for real-time data)"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            response = make_response(f(*args, **kwargs))
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            return response
        return decorated_function
    return decorator
