"""create_users_table

Revision ID: 9ea6200d21f9
Revises: b3bb642100bf
Create Date: 2026-04-05 20:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ea6200d21f9'
down_revision: Union[str, None] = 'b3bb642100bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('email', sa.String, unique=True, index=True, nullable=False),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('hashed_password', sa.String, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    )

    with op.batch_alter_table('expenses') as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer, nullable=True))
        batch_op.create_foreign_key('fk_expenses_user_id', 'users', ['user_id'], ['id'], ondelete='CASCADE')
        batch_op.create_index('ix_expenses_user_id', ['user_id'])


def downgrade() -> None:
    with op.batch_alter_table('expenses') as batch_op:
        batch_op.drop_index('ix_expenses_user_id')
        batch_op.drop_constraint('fk_expenses_user_id', type_='foreignkey')
        batch_op.drop_column('user_id')

    op.drop_table('users')
