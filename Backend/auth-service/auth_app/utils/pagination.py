from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size = 10  # Default items per page
    page_query_param = 'page'  # Query param for page number (e.g., ?page=2)
    page_size_query_param = 'size'  # Allow clients to set page size (e.g., ?size=20)
    max_page_size = 100  # Maximum page size allowed

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,  # Total number of items
            'total_pages': self.page.paginator.num_pages,  # Total number of pages
            'current_page': self.page.number,  # Current page number
            'next': self.get_next_link(),  # URL to next page
            'previous': self.get_previous_link(),  # URL to previous page
            'results': data  # Paginated data
        })