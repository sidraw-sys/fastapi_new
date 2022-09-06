"""add foreign key in posts table

Revision ID: 59486e530924
Revises: ea18169b11bc
Create Date: 2022-09-06 11:57:57.670395

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59486e530924'
down_revision = 'ea18169b11bc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_foreign_key("posts_users_fk", source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('posts_users_fk')
