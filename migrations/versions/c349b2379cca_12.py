"""12

Revision ID: c349b2379cca
Revises: 66eaedf79de8
Create Date: 2018-07-25 23:22:12.153400

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c349b2379cca'
down_revision = '66eaedf79de8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('jobs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('jobname', sa.String(length=64), nullable=True),
    sa.Column('func', sa.String(length=64), nullable=True),
    sa.Column('args', sa.String(length=64), nullable=True),
    sa.Column('jobtype', sa.String(length=64), nullable=True),
    sa.Column('trigger', sa.String(length=64), nullable=True),
    sa.Column('year', sa.String(length=64), nullable=True),
    sa.Column('month', sa.String(length=64), nullable=True),
    sa.Column('day', sa.String(length=64), nullable=True),
    sa.Column('hour', sa.String(length=64), nullable=True),
    sa.Column('minute', sa.String(length=64), nullable=True),
    sa.Column('second', sa.String(length=64), nullable=True),
    sa.Column('week', sa.String(length=64), nullable=True),
    sa.Column('day_of_week', sa.String(length=64), nullable=True),
    sa.Column('last_timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('job')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('job',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('jobname', mysql.VARCHAR(length=64), nullable=True),
    sa.Column('func', mysql.VARCHAR(length=64), nullable=True),
    sa.Column('args', mysql.VARCHAR(length=64), nullable=True),
    sa.Column('jobtype', mysql.VARCHAR(length=64), nullable=True),
    sa.Column('trigger', mysql.VARCHAR(length=64), nullable=True),
    sa.Column('year', mysql.VARCHAR(length=64), nullable=True),
    sa.Column('month', mysql.VARCHAR(length=64), nullable=True),
    sa.Column('day', mysql.VARCHAR(length=64), nullable=True),
    sa.Column('hour', mysql.VARCHAR(length=64), nullable=True),
    sa.Column('minute', mysql.VARCHAR(length=64), nullable=True),
    sa.Column('second', mysql.VARCHAR(length=64), nullable=True),
    sa.Column('week', mysql.VARCHAR(length=64), nullable=True),
    sa.Column('day_of_week', mysql.VARCHAR(length=64), nullable=True),
    sa.Column('last_timestamp', mysql.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.drop_table('jobs')
    # ### end Alembic commands ###
