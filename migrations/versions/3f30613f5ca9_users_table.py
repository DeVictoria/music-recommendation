"""users table

Revision ID: 3f30613f5ca9
Revises: 45f354244945
Create Date: 2024-06-15 01:12:15.113358

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f30613f5ca9'
down_revision = '45f354244945'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('genres',
               existing_type=sa.VARCHAR(length=256),
               type_=sa.PickleType(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('genres',
               existing_type=sa.PickleType(),
               type_=sa.VARCHAR(length=256),
               existing_nullable=False)

    # ### end Alembic commands ###
