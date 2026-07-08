"""change port and hostname to arrays

Revision ID: d31551932088
Revises: e5dc723f8ae0
Create Date: 2026-06-19 19:13:54.367046

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY


revision: str = 'd31551932088'
down_revision: Union[str, Sequence[str], None] = 'e5dc723f8ae0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('ALTER TABLE feeds ALTER COLUMN port TYPE INTEGER[] USING ARRAY[port]')
    op.execute('ALTER TABLE feeds ALTER COLUMN hostname TYPE VARCHAR[] USING ARRAY[hostname]')


def downgrade() -> None:
    op.execute('ALTER TABLE feeds ALTER COLUMN port TYPE INTEGER USING port[1]')
    op.execute('ALTER TABLE feeds ALTER COLUMN hostname TYPE VARCHAR USING hostname[1]')