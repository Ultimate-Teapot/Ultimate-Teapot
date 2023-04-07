from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class NewPaginator(PageNumberPagination):
    # not used
     def get_paginated_response(self, data):
        return Response(data)
 

    
 