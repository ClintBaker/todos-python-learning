"""add phone_number for user

Revision ID: 6b614b6d1318
Revises: 
Create Date: 2025-06-24 15:26:56.972461

"""
from typing import Sequence, Union
from alembic import op  # type: ignore

import sqlalchemy as sa #type: ignore


# revision identifiers, used by Alembic.
revision: str = '6b614b6d1318'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'phone_number')
