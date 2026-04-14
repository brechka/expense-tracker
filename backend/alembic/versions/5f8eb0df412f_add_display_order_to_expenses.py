"""add_display_order_to_expenses

Revision ID: 5f8eb0df412f
Revises: 84153160039d
Create Date: 2026-04-05 23:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '5f8eb0df412f'
down_revision: Union[str, None] = '84153160039d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('expenses') as batch_op:
        batch_op.add_column(sa.Column('display_order', sa.Integer, nullable=True))


def downgrade() -> None:
    with op.batch_alter_table('expenses') as batch_op:
        batch_op.drop_column('display_order')
