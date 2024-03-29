"""add photo to precipe step

Revision ID: 277e7264e24d
Revises: 05f7a3fa0c80
Create Date: 2024-03-26 15:00:16.834207

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '277e7264e24d'
down_revision = '05f7a3fa0c80'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('recipe_steps', schema=None) as batch_op:
        batch_op.add_column(sa.Column('photo_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_recipe_steps_photo_id_photos'), 'photos', ['photo_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('recipe_steps', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_recipe_steps_photo_id_photos'), type_='foreignkey')
        batch_op.drop_column('photo_id')

    # ### end Alembic commands ###
