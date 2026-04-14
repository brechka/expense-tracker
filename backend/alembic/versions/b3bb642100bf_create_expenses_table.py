"""create_expenses_table

Revision ID: b3bb642100bf
Revises: 
Create Date: 2026-03-16 14:55:05.790618

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b3bb642100bf'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'expenses',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('amount', sa.Float, nullable=False),
        sa.Column('currency', sa.String, nullable=False),
        sa.Column('category', sa.String, nullable=False),
        sa.Column('date', sa.String, nullable=False),
    )


def downgrade() -> None:
    op.drop_table('expenses')
