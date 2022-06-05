import typing

from django.core.paginator import Paginator, EmptyPage
from django.db.models import QuerySet

from core.api.schemas import PaginationBuilderSchema


def page_builder(queryset: QuerySet[typing.Any], per_page: int = 10, page_number: int = 1) -> PaginationBuilderSchema:
    paginator = Paginator(queryset, per_page)
    count = paginator.count
    total_pages = paginator.num_pages
    next_page = None
    previous_page = None

    if 0 < page_number <= total_pages:
        try:
            page = paginator.page(page_number)

            try:
                next_page = page.next_page_number()
            except EmptyPage:
                pass

            try:
                previous_page = page.previous_page_number()
            except EmptyPage:
                pass

            data = page.object_list

            return PaginationBuilderSchema(
                count=count,
                next_page=next_page,
                previous_page=previous_page,
                total_pages=total_pages,
                data=list(data)
            )
        except EmptyPage:
            pass

    return PaginationBuilderSchema(
        count=count,
        next_page=next_page,
        previous_page=previous_page,
        total_pages=total_pages,
        data=[]
    )
