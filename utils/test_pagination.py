from unittest import TestCase
from utils.pagination import make_pagination_range

class PaginationTest(TestCase):
    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qty_pages=4,
            current_page=1
        )['pagination']
        self.assertEqual([1,2,3,4], pagination)

    def test_make_pagination_first_range_is_static_if_current_page_is_less_than_middle_page(self):
        # Current page = 1 - Middle page = 2
        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qty_pages=4,
            current_page=1
        )['pagination']
        self.assertEqual([1,2,3,4], pagination)

        # Current page = 2 - Middle page = 2
        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qty_pages=4,
            current_page=2
        )['pagination']
        self.assertEqual([1,2,3,4], pagination)

        # Current page = 3 - Middle page = 3
        # Here change middle page
        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qty_pages=4,
            current_page=3
        )['pagination']
        self.assertEqual([2,3,4,5], pagination)

    def test_make_pagination_sure_middle_range_is_correct(self):
        # Current page = 10 - Middle page = 10
        # Here change middle page
        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qty_pages=4,
            current_page=10
        )['pagination']
        self.assertEqual([9,10,11,12], pagination)

        # Current page = 14 - Middle page = 14
        # Here change middle page
        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qty_pages=4,
            current_page=14
        )['pagination']
        self.assertEqual([13,14,15,16], pagination)

    def test_make_pagination_range_is_static_when_last_page_is_next(self):
        # Current page = 18 - Middle page = 18
        # Here change middle page
        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qty_pages=4,
            current_page=18
        )['pagination']
        self.assertEqual([17,18,19,20], pagination)

        # Current page = 19 - Middle page = 18
        # Here change middle page
        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qty_pages=4,
            current_page=19
        )['pagination']
        self.assertEqual([17,18,19,20], pagination)

        # Current page = 20 - Middle page = 18
        # Here change middle page
        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qty_pages=4,
            current_page=20
        )['pagination']
        self.assertEqual([17,18,19,20], pagination)

        # Current page = 21 - Middle page = 18
        # Here change middle page
        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qty_pages=4,
            current_page=21
        )['pagination']
        self.assertEqual([17,18,19,20], pagination)