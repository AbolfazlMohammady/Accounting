from rest_framework.pagination import PageNumberPagination


def get_pagination(queryset, request):
    """اعمال صفحه‌بندی برای کوئری‌ست داده‌شده"""
    paginator = PageNumberPagination()
    paginator.page_size = 6
    page_query = paginator.paginate_queryset(queryset, request)
    return paginator, page_query