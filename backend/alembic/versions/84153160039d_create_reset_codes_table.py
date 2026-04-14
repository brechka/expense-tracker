"""create_reset_codes_table

Revision ID: 84153160039d
Revises: cc7b0b2185a2
Create Date: 2026-04-05 22:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84153160039d'
down_revision: Union[str, None] = 'cc7b0b2185a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'reset_codes',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('code', sa.String, unique=True, index=True, nullable=False),
        sa.Column('expires_at', sa.DateTime, nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False),
        sa.Column('created_at', sa.DateTime),
        sa.Column('used', sa.Boolean, default=False),
    )


def downgrade() -> None:
    op.drop_table('reset_codes')
