# your_project/pagination.py
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from math import ceil

class CustomPagination(PageNumberPagination):
    page_size = 5  
    page_size_query_param = 'limit'
    page_query_param = 'page'  
    max_page_size = 100  

    def get_paginated_response(self, data):
        return Response({
            'message': 'Data retrieved successfully',
            'pagination': {
                'total_count': self.page.paginator.count,
                'current_page': self.page.number,
                'page_size': self.get_page_size(self.request),
                'total_pages': ceil(self.page.paginator.count / self.get_page_size(self.request)),
                'has_next': self.page.has_next(),
                'has_previous': self.page.has_previous(),
                'next_page': self.page.next_page_number() if self.page.has_next() else None,
                'previous_page': self.page.previous_page_number() if self.page.has_previous() else None,
            },
            'data': data  
        })