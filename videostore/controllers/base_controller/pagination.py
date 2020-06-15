from flask import request
from flask_sqlalchemy import BaseQuery as FlaskQuery
from flask_sqlalchemy import Pagination as FlaskPagination
from sqlalchemy.orm.query import Query as SAQuery

import paginate


class ListPaginator:
    """
    Paginator from paginate module, used for lists. Flask-SQLAlchemy queries
    come with their own
    """
    def __init__(self, obj):
        self.obj = obj

    def __getitem__(self, range):
        return self.obj[range]

    def __len__(self):
        return len(self.obj)


class ListPage(paginate.Page):
    """
    Paginator from paginate module, used for lists. Flask-SQLAlchemy queries
    come with their own
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, wrapper_class=ListPaginator, **kwargs)


class ResponsePaginator:
    """
    Perfoms pagination for current request
    works with:
        - SQLAlchemy query objects
        - Python iterables
        - Flask-SQLAlchemy query objects (which come with their own pagination)
    """

    def __init__(self, collection):
        self.collection = collection

    def page(self):
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        item_count = self._len()

        if isinstance(self.collection, SAQuery):
            if isinstance(self.collection, FlaskQuery):
                return self.collection.paginate(error_out=False)
            else:
                return FlaskPagination(
                    query=self.collection, page=page, per_page=per_page,
                    total=item_count,
                    items=self.collection.limit(per_page).offset((page - 1) * per_page).all()
                )

        return paginate.Page(
            self.collection, page=page, items_per_page=per_page,
            item_count=item_count
        )

    def _len(self):
        if isinstance(self.collection, SAQuery):
            return self.collection.count()
        return len(self.collection)

    def page_dict(self, fetch_all=False):
        if self.is_fetch_all or fetch_all:
            count = self._len()
            return {
                'objects': self.collection,
                'page': 1,
                'per_page': count,
                'total': count,
                'pages': 1
            }

        page = self.page()

        return {
            'objects': page.items,
            'page': page.page,
            'per_page': (
                getattr(page, 'items_per_page', None) or
                getattr(page, 'per_page')
            ),
            'total': (
                getattr(page, 'item_count', None) or
                getattr(page, 'total')
            ),
            'pages': (
                getattr(page, 'page_count', None) or
                getattr(page, 'pages')
            )
        }

    @property
    def is_fetch_all(self):
        return bool(
            str(request.args.get('all', '')).lower() == 'true' or
            str(request.args.get('paginate', '')).lower() == 'false'
        )
