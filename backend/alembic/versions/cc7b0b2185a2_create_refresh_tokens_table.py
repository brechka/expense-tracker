"""create_refresh_tokens_table

Revision ID: cc7b0b2185a2
Revises: 9ea6200d21f9
Create Date: 2026-04-05 21:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc7b0b2185a2'
down_revision: Union[str, None] = '9ea6200d21f9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'refresh_tokens',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('token', sa.String, unique=True, index=True, nullable=False),
        sa.Column('expires_at', sa.DateTime, nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False),
        sa.Column('created_at', sa.DateTime),
    )


def downgrade() -> None:
    op.drop_table('refresh_tokens')
