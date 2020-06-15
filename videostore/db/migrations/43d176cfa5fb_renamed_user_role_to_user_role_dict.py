"""Renamed User.role to User.role_dict

Revision ID: 43d176cfa5fb
Revises: 9651ddd5d59e
Create Date: 2017-01-20 09:12:15.372326

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '43d176cfa5fb'
down_revision = '9651ddd5d59e'
branch_labels = ()
depends_on = None


def upgrade():
    op.alter_column(
        table_name='users', column_name='role', new_column_name='role_enum'
    )

def downgrade():
    op.alter_column(
        table_name='users', column_name='role_enum', new_column_name='role'
    )
