"""Create_Index

Revision ID: a0b434293802
Revises: efcf193b578e
Create Date: 2023-03-18 13:28:58.482112

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0b434293802'
down_revision = 'efcf193b578e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('charityproject', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_charityproject_fully_invested'), ['fully_invested'], unique=False)

    with op.batch_alter_table('donation', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_donation_fully_invested'), ['fully_invested'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('donation', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_donation_fully_invested'))

    with op.batch_alter_table('charityproject', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_charityproject_fully_invested'))

    # ### end Alembic commands ###
