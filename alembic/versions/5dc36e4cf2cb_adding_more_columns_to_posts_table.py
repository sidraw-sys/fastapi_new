"""adding more columns to posts table

Revision ID: 5dc36e4cf2cb
Revises: c2219b0fd636
Create Date: 2022-09-06 11:29:23.205633

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5dc36e4cf2cb'
down_revision = 'c2219b0fd636'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String, nullable=False))
    op.add_column("posts", sa.Column("published", sa.Boolean, nullable=False, server_default='True'))
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))
    op.add_column("posts", sa.Column("owner_id", sa.Integer, nullable=False))


def downgrade() -> None:
    op.drop_column('posts','content')
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    op.drop_column('posts','owner_id')
