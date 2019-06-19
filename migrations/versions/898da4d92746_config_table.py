"""config table

Revision ID: 898da4d92746
Revises: 99dc7ef4b73f
Create Date: 2019-06-19 13:41:49.195146

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '898da4d92746'
down_revision = '99dc7ef4b73f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('config',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('entity', sa.String(length=128), nullable=True),
    sa.Column('value', sa.BLOB(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('config')
    # ### end Alembic commands ###
