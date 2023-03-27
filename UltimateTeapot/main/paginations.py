from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class NewPaginator(PageNumberPagination):
    # Set any other options you want here like page_size

    def get_paginated_response(self, data):
        return Response(data)
