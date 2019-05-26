"""empty message

Revision ID: c76c5c320902
Revises: 9ac2032d8e36
Create Date: 2019-05-26 10:00:33.457447

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c76c5c320902'
down_revision = '9ac2032d8e36'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article', sa.Column('image', sa.String(length=256), nullable=True))
    op.add_column('article', sa.Column('status', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('article', 'status')
    op.drop_column('article', 'image')
    # ### end Alembic commands ###