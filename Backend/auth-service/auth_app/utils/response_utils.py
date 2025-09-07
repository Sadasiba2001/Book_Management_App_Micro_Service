from copy import deepcopy
from rest_framework import status
from rest_framework.response import Response
from ..constants.response_template import SUCCESS_RESPONSE, ERROR_RESPONSE

class ResponseUtils:
    
    @staticmethod
    def success(message: str, data=None, http_status=status.HTTP_200_OK) -> Response:
        """
        Generating a standardized success response.
        
        Args:
            message (str): The success message.
            data (Any, optional): The data to include in the response. Defaults to None.
            http_status (int, optional): HTTP status code. Defaults to 200 OK.
        
        Returns:
            Response: A DRF Response object with the standardized success format.
        """
        response_data = deepcopy(SUCCESS_RESPONSE)
        response_data.update({
            "message": message,
            "data": data,
            "error": None
        })
        return Response(response_data, status=http_status)

    @staticmethod
    def error(message: str, error: str = None, http_status=status.HTTP_400_BAD_REQUEST) -> Response:
        """
        Generating a standardized error response.
        
        Args:
            message (str): The error message.
            error (str, optional): Additional error details. Defaults to None.
            http_status (int, optional): HTTP status code. Defaults to 400 Bad Request.
        
        Returns:
            Response: A DRF Response object with the standardized error format.
        """
        response_data = deepcopy(ERROR_RESPONSE)
        response_data.update({
            "message": message,
            "error": error,
            "data": None
        })
        return Response(response_data, status=http_status)