"""add order in change name price

Revision ID: a6ff183f0016
Revises: 4dfcfcb4e5f6
Create Date: 2024-07-01 16:29:33.118273

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a6ff183f0016'
down_revision: Union[str, None] = '4dfcfcb4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('carts', 'price',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=10, asdecimal=2),
               existing_nullable=False)
    op.alter_column('carts', 'total_price',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=10, asdecimal=2),
               existing_nullable=False)
    op.add_column('order', sa.Column('total_price', sa.Float(precision=10, asdecimal=2), nullable=False))
    op.drop_column('order', 'unit_price')
    op.alter_column('payments', 'amount',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=10, asdecimal=3),
               existing_nullable=False)
    op.alter_column('products', 'product_price',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=10, asdecimal=2),
               existing_nullable=False)
    op.alter_column('products', 'discount_percent',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=5, asdecimal=2),
               existing_nullable=False)
    op.alter_column('products', 'discount_price',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=10, asdecimal=2),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('products', 'discount_price',
               existing_type=sa.Float(precision=10, asdecimal=2),
               type_=sa.REAL(),
               existing_nullable=False)
    op.alter_column('products', 'discount_percent',
               existing_type=sa.Float(precision=5, asdecimal=2),
               type_=sa.REAL(),
               existing_nullable=False)
    op.alter_column('products', 'product_price',
               existing_type=sa.Float(precision=10, asdecimal=2),
               type_=sa.REAL(),
               existing_nullable=False)
    op.alter_column('payments', 'amount',
               existing_type=sa.Float(precision=10, asdecimal=3),
               type_=sa.REAL(),
               existing_nullable=False)
    op.add_column('order', sa.Column('unit_price', sa.REAL(), autoincrement=False, nullable=False))
    op.drop_column('order', 'total_price')
    op.alter_column('carts', 'total_price',
               existing_type=sa.Float(precision=10, asdecimal=2),
               type_=sa.REAL(),
               existing_nullable=False)
    op.alter_column('carts', 'price',
               existing_type=sa.Float(precision=10, asdecimal=2),
               type_=sa.REAL(),
               existing_nullable=False)
    # ### end Alembic commands ###
