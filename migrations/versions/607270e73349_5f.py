"""5f

Revision ID: 607270e73349
Revises: 4c4ae1163f8c
Create Date: 2018-07-03 00:23:50.384703

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '607270e73349'
down_revision = '4c4ae1163f8c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('body_html', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'body_html')
    # ### end Alembic commands ###
