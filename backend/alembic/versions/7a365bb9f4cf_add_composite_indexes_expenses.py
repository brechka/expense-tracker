"""add_composite_indexes_expenses

Revision ID: 7a365bb9f4cf
Revises: 5f8eb0df412f
Create Date: 2026-04-06 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


revision: str = '7a365bb9f4cf'
down_revision: Union[str, None] = '5f8eb0df412f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index('ix_expenses_user_order', 'expenses', ['user_id', 'display_order'])
    op.create_index('ix_expenses_user_date', 'expenses', ['user_id', 'date'])


def downgrade() -> None:
    op.drop_index('ix_expenses_user_date', 'expenses')
    op.drop_index('ix_expenses_user_order', 'expenses')
