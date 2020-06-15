from flask.ext.sqlalchemy import BaseQuery as FlaskSqlAlchemyBaseQuery


class BaseQuery(FlaskSqlAlchemyBaseQuery):

    @property
    def model(self):
        return self.column_descriptions[0]['entity']
