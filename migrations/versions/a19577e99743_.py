"""empty message

Revision ID: a19577e99743
Revises: 
Create Date: 2023-03-17 15:20:54.369447

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a19577e99743'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('circuits',
    sa.Column('circuitId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('circuitRef', sa.String(length=255), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('location', sa.String(length=255), nullable=True),
    sa.Column('country', sa.String(length=255), nullable=True),
    sa.Column('lat', sa.Float(), nullable=True),
    sa.Column('lng', sa.Float(), nullable=True),
    sa.Column('alt', sa.Integer(), nullable=True),
    sa.Column('url', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('circuitId')
    )
    op.create_table('constructors',
    sa.Column('constructorId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('constructorRef', sa.String(length=255), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('nationality', sa.String(length=255), nullable=True),
    sa.Column('url', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('constructorId')
    )
    op.create_table('drivers',
    sa.Column('driverId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('driverRef', sa.String(length=255), nullable=False),
    sa.Column('number', sa.Integer(), nullable=True),
    sa.Column('code', sa.String(length=3), nullable=True),
    sa.Column('forename', sa.String(length=255), nullable=False),
    sa.Column('surname', sa.String(length=255), nullable=False),
    sa.Column('dob', sa.Date(), nullable=True),
    sa.Column('nationality', sa.String(length=255), nullable=True),
    sa.Column('url', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('driverId'),
    sa.UniqueConstraint('driverRef')
    )
    op.create_table('seasons',
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('year')
    )
    op.create_table('status',
    sa.Column('statusId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('status', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('statusId')
    )
    op.create_table('trackstatus',
    sa.Column('statusId', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('statusId')
    )
    op.create_table('races',
    sa.Column('raceId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('round', sa.Integer(), nullable=False),
    sa.Column('circuitId', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('time', sa.Time(), nullable=True),
    sa.Column('url', sa.String(length=255), nullable=True),
    sa.Column('fp1_date', sa.Date(), nullable=True),
    sa.Column('fp1_time', sa.Time(), nullable=True),
    sa.Column('fp2_date', sa.Date(), nullable=True),
    sa.Column('fp2_time', sa.Time(), nullable=True),
    sa.Column('fp3_date', sa.Date(), nullable=True),
    sa.Column('fp3_time', sa.Time(), nullable=True),
    sa.Column('quali_date', sa.Date(), nullable=True),
    sa.Column('quali_time', sa.Time(), nullable=True),
    sa.Column('sprint_date', sa.Date(), nullable=True),
    sa.Column('sprint_time', sa.Time(), nullable=True),
    sa.ForeignKeyConstraint(['circuitId'], ['circuits.circuitId'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['year'], ['seasons.year'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('raceId')
    )
    op.create_table('constructorresults',
    sa.Column('constructorResultsId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('raceId', sa.Integer(), nullable=False),
    sa.Column('constructorId', sa.Integer(), nullable=False),
    sa.Column('points', sa.Float(), nullable=True),
    sa.Column('status', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['constructorId'], ['constructors.constructorId'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['raceId'], ['races.raceId'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('constructorResultsId')
    )
    op.create_table('constructorstandings',
    sa.Column('constructorStandingsId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('raceId', sa.Integer(), nullable=False),
    sa.Column('constructorId', sa.Integer(), nullable=False),
    sa.Column('points', sa.Float(), nullable=False),
    sa.Column('position', sa.Integer(), nullable=True),
    sa.Column('positionText', sa.String(length=255), nullable=True),
    sa.Column('wins', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['constructorId'], ['constructors.constructorId'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['raceId'], ['races.raceId'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('constructorStandingsId')
    )
    op.create_table('driverstandings',
    sa.Column('driverStandingsId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('raceId', sa.Integer(), nullable=False),
    sa.Column('driverId', sa.Integer(), nullable=False),
    sa.Column('points', sa.Float(), nullable=False),
    sa.Column('position', sa.Integer(), nullable=True),
    sa.Column('positionText', sa.String(length=255), nullable=True),
    sa.Column('wins', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['driverId'], ['drivers.driverId'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['raceId'], ['races.raceId'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('driverStandingsId')
    )
    op.create_table('laps',
    sa.Column('lapId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('raceId', sa.Integer(), nullable=False),
    sa.Column('time', sa.String(length=22), nullable=True),
    sa.Column('driver', sa.String(length=3), nullable=True),
    sa.Column('drivernumber', sa.String(length=3), nullable=True),
    sa.Column('laptime', sa.String(length=22), nullable=True),
    sa.Column('lapnumber', sa.Integer(), nullable=True),
    sa.Column('stint', sa.Integer(), nullable=True),
    sa.Column('pitouttime', sa.String(length=22), nullable=True),
    sa.Column('pitintime', sa.String(length=22), nullable=True),
    sa.Column('sector1time', sa.String(length=22), nullable=True),
    sa.Column('sector2time', sa.String(length=22), nullable=True),
    sa.Column('sector3time', sa.String(length=22), nullable=True),
    sa.Column('sector1sessiontime', sa.String(length=22), nullable=True),
    sa.Column('sector2sessiontime', sa.String(length=22), nullable=True),
    sa.Column('sector3sessiontime', sa.String(length=22), nullable=True),
    sa.Column('speedi1', sa.Float(), nullable=True),
    sa.Column('speedi2', sa.Float(), nullable=True),
    sa.Column('speedfl', sa.Float(), nullable=True),
    sa.Column('speedst', sa.Float(), nullable=True),
    sa.Column('ispersonalbest', sa.Boolean(), nullable=True),
    sa.Column('compound', sa.String(length=10), nullable=True),
    sa.Column('tyrelife', sa.Float(), nullable=True),
    sa.Column('freshtyre', sa.Boolean(), nullable=True),
    sa.Column('team', sa.String(length=255), nullable=True),
    sa.Column('lapstarttime', sa.String(length=22), nullable=True),
    sa.Column('lapstartdate', sa.String(length=22), nullable=True),
    sa.Column('trackstatus', sa.Integer(), nullable=True),
    sa.Column('isaccurate', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['raceId'], ['races.raceId'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('lapId')
    )
    op.create_table('pitstops',
    sa.Column('raceId', sa.Integer(), nullable=False),
    sa.Column('driverId', sa.Integer(), nullable=False),
    sa.Column('stop', sa.Integer(), nullable=False),
    sa.Column('lap', sa.Integer(), nullable=False),
    sa.Column('time', sa.Integer(), nullable=True),
    sa.Column('duration', sa.String(length=255), nullable=True),
    sa.Column('milliseconds', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['driverId'], ['drivers.driverId'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['raceId'], ['races.raceId'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('raceId', 'driverId', 'stop')
    )
    op.create_table('qualifying',
    sa.Column('qualifyId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('raceId', sa.Integer(), nullable=False),
    sa.Column('driverId', sa.Integer(), nullable=False),
    sa.Column('constructorId', sa.Integer(), nullable=False),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('position', sa.Integer(), nullable=True),
    sa.Column('q1', sa.String(length=255), nullable=True),
    sa.Column('q2', sa.String(length=255), nullable=True),
    sa.Column('q3', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['constructorId'], ['constructors.constructorId'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['driverId'], ['drivers.driverId'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['raceId'], ['races.raceId'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('qualifyId')
    )
    op.create_table('results',
    sa.Column('resultId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('raceId', sa.Integer(), nullable=False),
    sa.Column('driverId', sa.Integer(), nullable=False),
    sa.Column('constructorId', sa.Integer(), nullable=False),
    sa.Column('number', sa.Integer(), nullable=True),
    sa.Column('grid', sa.Integer(), nullable=False),
    sa.Column('position', sa.Integer(), nullable=True),
    sa.Column('positionText', sa.String(length=255), nullable=False),
    sa.Column('positionOrder', sa.Integer(), nullable=False),
    sa.Column('points', sa.Integer(), nullable=False),
    sa.Column('laps', sa.Integer(), nullable=False),
    sa.Column('time', sa.String(length=255), nullable=True),
    sa.Column('milliseconds', sa.Integer(), nullable=True),
    sa.Column('fastestLap', sa.Integer(), nullable=True),
    sa.Column('rank', sa.Integer(), nullable=True),
    sa.Column('fastestLapTime', sa.Integer(), nullable=True),
    sa.Column('fastestLapSpeed', sa.Integer(), nullable=True),
    sa.Column('statusId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['constructorId'], ['constructors.constructorId'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['driverId'], ['drivers.driverId'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['raceId'], ['races.raceId'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['statusId'], ['status.statusId'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('resultId')
    )
    op.create_table('sprintresults',
    sa.Column('sprintResultId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('raceId', sa.Integer(), nullable=False),
    sa.Column('driverId', sa.Integer(), nullable=False),
    sa.Column('constructorId', sa.Integer(), nullable=False),
    sa.Column('number', sa.Integer(), nullable=True),
    sa.Column('grid', sa.Integer(), nullable=False),
    sa.Column('position', sa.Integer(), nullable=True),
    sa.Column('positionText', sa.String(length=255), nullable=False),
    sa.Column('positionOrder', sa.Integer(), nullable=False),
    sa.Column('points', sa.Integer(), nullable=False),
    sa.Column('laps', sa.Integer(), nullable=False),
    sa.Column('time', sa.String(length=255), nullable=True),
    sa.Column('milliseconds', sa.Integer(), nullable=True),
    sa.Column('fastestLap', sa.Integer(), nullable=True),
    sa.Column('fastestLapTime', sa.Integer(), nullable=True),
    sa.Column('statusId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['constructorId'], ['constructors.constructorId'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['driverId'], ['drivers.driverId'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['raceId'], ['races.raceId'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['statusId'], ['status.statusId'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('sprintResultId')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sprintresults')
    op.drop_table('results')
    op.drop_table('qualifying')
    op.drop_table('pitstops')
    op.drop_table('laps')
    op.drop_table('driverstandings')
    op.drop_table('constructorstandings')
    op.drop_table('constructorresults')
    op.drop_table('races')
    op.drop_table('trackstatus')
    op.drop_table('status')
    op.drop_table('seasons')
    op.drop_table('drivers')
    op.drop_table('constructors')
    op.drop_table('circuits')
    # ### end Alembic commands ###
