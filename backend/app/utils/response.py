"""
Response utility functions for consistent API responses
"""
from flask import jsonify
from typing import Any, Dict


def success_response(data: Dict[str, Any], status_code: int = 200):
    """Return a success response"""
    response = {
        'success': True,
        'data': data
    }
    return jsonify(response), status_code


def error_response(message: str, status_code: int = 400, errors: Dict = None):
    """Return an error response"""
    response = {
        'success': False,
        'error': {
            'message': message,
            'code': status_code
        }
    }

    if errors:
        response['error']['details'] = errors

    return jsonify(response), status_code
