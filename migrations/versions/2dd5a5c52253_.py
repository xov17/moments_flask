"""empty message

Revision ID: 2dd5a5c52253
Revises: 78ab59ef17c9
Create Date: 2016-12-30 00:46:34.630296

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2dd5a5c52253'
down_revision = '78ab59ef17c9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tag',
    sa.Column('tag', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('tag')
    )
    op.create_table('postTags',
    sa.Column('tag', sa.String(length=200), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['tag'], ['tag.tag'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('postTags')
    op.drop_table('tag')
    # ### end Alembic commands ###
