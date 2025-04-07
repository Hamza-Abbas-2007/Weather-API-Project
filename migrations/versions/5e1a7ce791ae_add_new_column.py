"""Add new column

Revision ID: 5e1a7ce791ae
Revises: 
Create Date: 2025-04-07 22:47:15.315017

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e1a7ce791ae'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('todo', schema=None) as batch_op:
        batch_op.add_column(sa.Column('Humidity', sa.String(length=200), nullable=False, server_default='Unknown'))


    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('todo', schema=None) as batch_op:
        batch_op.drop_column('Humidity')

    # ### end Alembic commands ###
