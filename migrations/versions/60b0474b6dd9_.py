"""empty message

Revision ID: 60b0474b6dd9
Revises: 
Create Date: 2023-03-13 14:59:19.666235

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60b0474b6dd9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('circuits',
    sa.Column('circuitId', sa.Integer(), nullable=False),
    sa.Column('circuitRef', sa.String(length=255), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('location', sa.String(length=255), nullable=True),
    sa.Column('country', sa.String(length=255), nullable=True),
    sa.Column('lat', sa.FLOAT(), nullable=True),
    sa.Column('lng', sa.FLOAT(), nullable=True),
    sa.Column('alt', sa.Integer(), nullable=True),
    sa.Column('url', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('circuitId')
    )
    op.create_table('constructors',
    sa.Column('constructorId', sa.Integer(), nullable=False),
    sa.Column('constructorRef', sa.String(length=255), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('nationality', sa.String(length=255), nullable=True),
    sa.Column('url', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('constructorId')
    )
    op.create_table('seasons',
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('year')
    )
    op.create_table('races',
    sa.Column('raceId', sa.Integer(), nullable=False),
    sa.Column('year', sa.Integer(), nullable=True),
    sa.Column('round', sa.Integer(), nullable=True),
    sa.Column('circuitId', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('date', sa.DATE(), nullable=True),
    sa.Column('time', sa.TIME(), nullable=True),
    sa.Column('url', sa.String(length=255), nullable=True),
    sa.Column('fp1_date', sa.DATE(), nullable=True),
    sa.Column('fp1_time', sa.TIME(), nullable=True),
    sa.Column('fp2_date', sa.DATE(), nullable=True),
    sa.Column('fp2_time', sa.TIME(), nullable=True),
    sa.Column('fp3_date', sa.DATE(), nullable=True),
    sa.Column('fp3_time', sa.TIME(), nullable=True),
    sa.Column('quali_date', sa.DATE(), nullable=True),
    sa.Column('quali_time', sa.TIME(), nullable=True),
    sa.Column('sprint_date', sa.DATE(), nullable=True),
    sa.Column('sprint_time', sa.TIME(), nullable=True),
    sa.ForeignKeyConstraint(['circuitId'], ['circuits.circuitId'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['year'], ['seasons.year'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('raceId')
    )
    op.create_table('constructorresults',
    sa.Column('constructorResultsId', sa.Integer(), nullable=False),
    sa.Column('raceId', sa.Integer(), nullable=False),
    sa.Column('constructorId', sa.Integer(), nullable=False),
    sa.Column('points', sa.FLOAT(), nullable=True),
    sa.Column('status', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['constructorId'], ['constructors.constructorId'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['raceId'], ['races.raceId'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('constructorResultsId')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('constructorresults')
    op.drop_table('races')
    op.drop_table('seasons')
    op.drop_table('constructors')
    op.drop_table('circuits')
    # ### end Alembic commands ###
