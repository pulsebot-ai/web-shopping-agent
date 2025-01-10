"""init

Revision ID: 186e51d77e14
Revises: 
Create Date: 2024-11-15 18:27:24.506293

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '186e51d77e14'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chats',
    sa.Column('id', sa.String(length=255), nullable=False),
    sa.Column('chat', mysql.LONGTEXT(), nullable=True),
    sa.Column('created_at', sa.BigInteger(), nullable=True),
    sa.Column('updated_at', sa.BigInteger(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('chats')
    # ### end Alembic commands ###
