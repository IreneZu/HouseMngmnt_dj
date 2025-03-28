"""slug_change

Revision ID: f3e17236ef41
Revises: 7bccf0443871
Create Date: 2025-01-20 12:10:01.421157

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3e17236ef41'
down_revision: Union[str, None] = '7bccf0443871'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_specifications_expenses_building_id'), 'specifications_expenses', ['building_id'], unique=False)
    op.create_index(op.f('ix_specifications_expenses_item_id'), 'specifications_expenses', ['item_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_specifications_expenses_item_id'), table_name='specifications_expenses')
    op.drop_index(op.f('ix_specifications_expenses_building_id'), table_name='specifications_expenses')
    # ### end Alembic commands ###
