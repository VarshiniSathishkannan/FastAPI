"""create table posts_using_alembic

Revision ID: a982a85905a8
Revises: 
Create Date: 2024-12-07 17:44:45.223387

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a982a85905a8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts_using_alembic',sa.Column('id',sa.Integer(),nullable=False,primary_key=True),sa.Column('title',sa.String(),nullable=False),sa.Column('content',sa.String(),nullable=False))


def downgrade() -> None:
    op.drop_table("posts_using_alembic")
    pass