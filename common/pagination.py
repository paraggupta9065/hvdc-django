from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'

    def get_paginated_data(self, serializer, data):
        data = super().get_paginated_data(serializer)
        data[data] = data
        return data
