from rest_framework.pagination import PageNumberPagination, _get_page_links
from rest_framework.utils.urls import remove_query_param, replace_query_param
from rest_framework.response import Response
from collections import OrderedDict


class DefaultPagination(PageNumberPagination):
    page_size = 18
