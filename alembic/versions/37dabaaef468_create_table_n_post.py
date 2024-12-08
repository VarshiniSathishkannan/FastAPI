"""create table n_post

Revision ID: 37dabaaef468
Revises: a982a85905a8
Create Date: 2024-12-07 17:55:40.285152

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '37dabaaef468'
down_revision: Union[str, None] = 'a982a85905a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('nposts',sa.Column('id',sa.Integer(),nullable=False,primary_key=True),sa.Column('title',sa.String(),nullable=False),sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('nposts')
    pass
