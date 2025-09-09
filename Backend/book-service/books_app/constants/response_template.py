"""
Constants for API response structures.
"""

"""
Template for a successful API response.
"""
SUCCESS_RESPONSE = {
    "status": "success",
    "message": "",
    "data": None,
    "error": None
}

"""
Template for an unsuccessful or error API response.
"""
ERROR_RESPONSE = {
    "status": "error",
    "message": "",
    "data": None,
    "error": None
}

