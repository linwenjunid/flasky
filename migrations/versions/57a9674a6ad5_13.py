"""13

Revision ID: 57a9674a6ad5
Revises: 28d0db10d49e
Create Date: 2018-08-01 19:32:41.997130

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57a9674a6ad5'
down_revision = '28d0db10d49e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('jobs', sa.Column('is_enable', sa.Boolean(), nullable=True))
    op.add_column('jobs', sa.Column('status', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('jobs', 'status')
    op.drop_column('jobs', 'is_enable')
    # ### end Alembic commands ###
