"""add alias for user

Revision ID: 05f7a3fa0c80
Revises: d51101854749
Create Date: 2024-02-26 10:34:33.350371

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05f7a3fa0c80'
down_revision = 'd51101854749'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('alias', sa.String(length=64), nullable=True))

    op.execute("UPDATE users SET alias = '' WHERE alias IS NULL")

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('alias', existing_type=sa.String(length=64), nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('alias')

    # ### end Alembic commands ###
