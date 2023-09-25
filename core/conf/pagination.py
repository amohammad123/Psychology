from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class DefaultPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 15


class CustomItemPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 15

    def get_paginated_response(self, data):
        return Response(
            {
                'data': data,
                # "links": {
                #     "next": self.get_next_link(),
                #     "previous": self.get_previous_link(),
                # },
                "total_items": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
            }
        )
