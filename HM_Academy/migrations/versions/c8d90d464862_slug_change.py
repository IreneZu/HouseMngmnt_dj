"""slug_change

Revision ID: c8d90d464862
Revises: f3e17236ef41
Create Date: 2025-01-20 12:32:48.279408

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c8d90d464862'
down_revision: Union[str, None] = 'f3e17236ef41'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('specifications_building', 'id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               nullable=False,
               autoincrement=True)
    op.alter_column('specifications_building', 'title',
               existing_type=sa.TEXT(),
               type_=sa.String(),
               existing_nullable=True)
    op.alter_column('specifications_building', 'number_of_floors',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=True)
    op.alter_column('specifications_building', 'number_of_entrances',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=True)
    op.alter_column('specifications_building', 'number_of_elevators',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=True)
    op.alter_column('specifications_building', 'number_of_chutes',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=True)
    op.alter_column('specifications_building', 'number_of_residents',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=True)
    op.alter_column('specifications_building', 'cleaning_area',
               existing_type=sa.TEXT(),
               type_=sa.Float(),
               existing_nullable=True)
    op.alter_column('specifications_building', 'residential_area',
               existing_type=sa.TEXT(),
               type_=sa.Float(),
               existing_nullable=True)
    op.create_index(op.f('ix_specifications_building_id'), 'specifications_building', ['id'], unique=False)
    op.create_index(op.f('ix_specifications_building_title'), 'specifications_building', ['title'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_specifications_building_title'), table_name='specifications_building')
    op.drop_index(op.f('ix_specifications_building_id'), table_name='specifications_building')
    op.alter_column('specifications_building', 'residential_area',
               existing_type=sa.Float(),
               type_=sa.TEXT(),
               existing_nullable=True)
    op.alter_column('specifications_building', 'cleaning_area',
               existing_type=sa.Float(),
               type_=sa.TEXT(),
               existing_nullable=True)
    op.alter_column('specifications_building', 'number_of_residents',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=True)
    op.alter_column('specifications_building', 'number_of_chutes',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=True)
    op.alter_column('specifications_building', 'number_of_elevators',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=True)
    op.alter_column('specifications_building', 'number_of_entrances',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=True)
    op.alter_column('specifications_building', 'number_of_floors',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=True)
    op.alter_column('specifications_building', 'title',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               existing_nullable=True)
    op.alter_column('specifications_building', 'id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               nullable=True,
               autoincrement=True)
    # ### end Alembic commands ###
