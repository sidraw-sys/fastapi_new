"""create posts table

Revision ID: c2219b0fd636
Revises: 
Create Date: 2022-09-06 11:19:15.131564

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2219b0fd636'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer, nullable=False, primary_key=True),
                             sa.Column('title', sa.String, nullable=False)
                    )


def downgrade() -> None:
    op.drop_table('posts')
