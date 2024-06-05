"""empty message

Revision ID: 54ab21b8ee75
Revises: 
Create Date: 2024-06-01 16:51:37.953258

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54ab21b8ee75'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transfer_rumor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('player_id', sa.Integer(), nullable=True),
    sa.Column('source_club', sa.String(length=100), nullable=True),
    sa.Column('destination_club', sa.String(length=100), nullable=True),
    sa.Column('transfer_fee', sa.String(length=20), nullable=True),
    sa.Column('rumor_details', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transfer_rumor')
    # ### end Alembic commands ###
