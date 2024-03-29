"""add Plant category

Revision ID: f29fe8019ee7
Revises: 51a453f5f1d5
Create Date: 2024-01-29 14:46:58.920400

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f29fe8019ee7'
down_revision = '51a453f5f1d5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('plant_categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('svg_icon', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_plant_categories'))
    )
    with op.batch_alter_table('plant_categories', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_plant_categories_name'), ['name'], unique=True)

    op.create_table('plant_family_categories',
    sa.Column('plant_family_id', sa.Integer(), nullable=False),
    sa.Column('plant_category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['plant_category_id'], ['plant_categories.id'], name=op.f('fk_plant_family_categories_plant_category_id_plant_categories')),
    sa.ForeignKeyConstraint(['plant_family_id'], ['plant_families.id'], name=op.f('fk_plant_family_categories_plant_family_id_plant_families')),
    sa.PrimaryKeyConstraint('plant_family_id', 'plant_category_id', name=op.f('pk_plant_family_categories'))
    )
    op.create_table('plant_variety_categories',
    sa.Column('plant_category_id', sa.Integer(), nullable=False),
    sa.Column('plant_variety_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['plant_category_id'], ['plant_categories.id'], name=op.f('fk_plant_variety_categories_plant_category_id_plant_categories')),
    sa.ForeignKeyConstraint(['plant_variety_id'], ['plant_varieties.id'], name=op.f('fk_plant_variety_categories_plant_variety_id_plant_varieties')),
    sa.PrimaryKeyConstraint('plant_category_id', 'plant_variety_id', name=op.f('pk_plant_variety_categories'))
    )
    with op.batch_alter_table('plant_families', schema=None) as batch_op:
        batch_op.drop_column('type_of')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('plant_families', schema=None) as batch_op:
        batch_op.add_column(sa.Column('type_of', sa.VARCHAR(length=16), nullable=False))

    op.drop_table('plant_variety_categories')
    op.drop_table('plant_family_categories')
    with op.batch_alter_table('plant_categories', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_plant_categories_name'))

    op.drop_table('plant_categories')
    # ### end Alembic commands ###
