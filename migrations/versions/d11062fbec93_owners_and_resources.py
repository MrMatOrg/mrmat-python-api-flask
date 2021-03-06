"""Owners and Resources

Revision ID: d11062fbec93
Revises: 4594cf7d8bfb
Create Date: 2021-06-26 17:57:31.057034

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd11062fbec93'
down_revision = '4594cf7d8bfb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('owners',
    sa.Column('id', sa.BigInteger().with_variant(sa.Integer(), 'sqlite'), nullable=False),
    sa.Column('client_id', sa.String(length=255), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('client_id')
    )
    op.add_column('resources', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.alter_column('resources', 'name',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.create_foreign_key(None, 'resources', 'owners', ['owner_id'], ['id'])
    op.drop_column('resources', 'owner')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('resources', sa.Column('owner', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'resources', type_='foreignkey')
    op.alter_column('resources', 'name',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    op.drop_column('resources', 'owner_id')
    op.drop_table('owners')
    # ### end Alembic commands ###
