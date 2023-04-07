from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, Date, Time, Boolean
from sqlalchemy.orm import validates
from app import db
    
# here i define my data as objects. this information will be used to create my tables. 
# this will make it easier to deply my database and apply changes to the schema. 
class Circuit(db.Model):
    # define the table name.
    __tablename__ = 'circuits'
    circuitId = Column(Integer, primary_key=True, autoincrement=True)
    circuitRef = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    location = Column(String(255))
    country = Column(String(255))
    lat = Column(Float)
    lng = Column(Float)
    alt = Column(Integer)
    url = Column(String(255), nullable=False)

    # add a to string method.
    def __str__(self):
        return self.name
    

class ConstructorResult(db.Model):
    __tablename__ = 'constructorresults'
    constructorResultsId = Column(Integer, primary_key=True, autoincrement=True)
    raceId = Column(Integer, ForeignKey('races.raceId', ondelete="CASCADE"), nullable=False, default=0)
    constructorId = Column(Integer, ForeignKey('constructors.constructorId', ondelete="CASCADE"), nullable=False, default=0)
    points = Column(Float)
    status = Column(String(255))

    def __str__(self):
        return self.constructorResultsId
    
    
class ConstructorStanding(db.Model):
    __tablename__ = 'constructorstandings'
    constructorStandingsId = Column(Integer, primary_key=True, autoincrement=True)
    raceId = Column(Integer, ForeignKey('races.raceId', ondelete="CASCADE"), nullable=False, default=0)
    constructorId = Column(Integer, ForeignKey('constructors.constructorId', ondelete="CASCADE"), nullable=False, default=0)
    points = Column(Float, nullable=False, default=0)
    position = Column(Integer)
    positionText = Column(String(255))
    wins = Column(Integer, nullable=False, default=0)

    def __str__(self):
        return self.constructorStandingsId
    

class Constructor(db.Model):
    __tablename__ = 'constructors'
    constructorId = Column(Integer, primary_key=True, autoincrement=True)
    constructorRef = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    nationality = Column(String(255))
    url = Column(String(255), nullable=False)

    def __str__(self):
        return self.name
    

class DriverStanding(db.Model):
    __tablename__ = 'driverstandings'
    driverStandingsId = Column(Integer, primary_key=True, autoincrement=True)
    raceId = Column(Integer, ForeignKey('races.raceId', ondelete="CASCADE"), nullable=False, default=0)
    driverId = Column(Integer, ForeignKey('drivers.driverId', ondelete="CASCADE"), nullable=False, default=0)
    points = Column(Float, nullable=False, default=0)
    position = Column(Integer)
    positionText = Column(String(255))
    wins = Column(Integer, nullable=False, default=0)

    def __str__(self):
        return self.driverStandingsId
    
    
class Driver(db.Model):
    __tablename__ = 'drivers'
    driverId = Column(Integer, primary_key=True, autoincrement=True)
    driverRef = Column(String(255), nullable=False, unique=True)
    number = Column(Integer)
    code = Column(String(3))
    forename = Column(String(255), nullable=False)
    surname = Column(String(255), nullable=False)
    dob = Column(Date)
    nationality = Column(String(255))
    url = Column(String(255), nullable=False)

    def __str__(self):
        return self.code
    
    
class Lap(db.Model):
    __tablename__ = 'laps'
    # lap times provided by fastf1
    lapId = Column(Integer, primary_key=True, autoincrement=True)
    raceId = Column(Integer, ForeignKey('races.raceId', ondelete="CASCADE"), nullable=False, default=0)
    time = Column(String(22))
    driver = Column(String(3))
    drivernumber = Column(String(3))
    laptime = Column(String(22))
    lapnumber = Column(Integer)
    stint = Column(Integer)
    pitouttime = Column(String(22))
    pitintime = Column(String(22))
    sector1time = Column(String(22))
    sector2time = Column(String(22))
    sector3time = Column(String(22))
    sector1sessiontime = Column(String(22))
    sector2sessiontime = Column(String(22))
    sector3sessiontime  = Column(String(22))
    speedi1  = Column(Float)
    speedi2  = Column(Float)
    speedfl  = Column(Float)
    speedst  = Column(Float)
    ispersonalbest = Column(Boolean)
    compound = Column(String(10))
    tyrelife  = Column(Float)
    freshtyre = Column(Boolean)
    team = Column(String(255))
    lapstarttime = Column(String(22))
    lapstartdate = Column(String(22))
    trackstatus = Column(Integer)
    isaccurate = Column(Boolean)    

    def __str__(self):
        return f"(lapId={self.lapId}, raceId={self.raceId}, lapnumber={self.lapnumber}, driver='{self.driver}', team='{self.team}', compound='{self.compound}', laptime={self.laptime}, time={self.time})"
    
    def as_dict(self):
        return {
            'lapId': self.lapId,
            'raceId': self.raceId,
            'lapnumber': self.lapnumber,
            'driver': self.driver,
            'team': self.team,
            'compound': self.compound,
            'laptime': self.laptime,
            'time': self.time
        }
    
class TrackStatus(db.Model):
    # sample: ‘1’: track clear, ‘2’: yellow flag, ‘3’: unused, ‘4’: safety car, ‘5’: red flag, ‘6’: vsc, ‘7’: vsc ending
    __tablename__ = 'trackstatus'
    statusId = Column(Integer, primary_key=True)
    status = Column(String(50))

    def __str__(self):
        return self.status
    

class PitStop(db.Model):
    __tablename__ = 'pitstops'
    raceId = Column(Integer, ForeignKey('races.raceId', ondelete="CASCADE"), nullable=False, default=0, primary_key=True)
    driverId = Column(Integer, ForeignKey('drivers.driverId', ondelete="CASCADE"), nullable=False, primary_key=True)
    stop = Column(Integer, nullable=False, primary_key=True)
    lap = Column(Integer, nullable=False)
    time = Column(Integer)
    duration = Column(String(255))
    milliseconds = Column(Integer)

    def __str__(self):
        return self.raceId
    
    
class Qualifying(db.Model):
    __tablename__ = 'qualifying'
    qualifyId = Column(Integer, primary_key=True, autoincrement=True)
    raceId = Column(Integer, ForeignKey('races.raceId', ondelete="CASCADE"), nullable=False, default=0)
    driverId = Column(Integer, ForeignKey('drivers.driverId', ondelete="CASCADE"), nullable=False, default=0)
    constructorId = Column(Integer, ForeignKey('constructors.constructorId', ondelete="CASCADE"), nullable=False, default=0)
    number = Column(Integer, nullable=False, default=0)
    position = Column(Integer)
    q1 = Column(String(255))
    q2 = Column(String(255))
    q3 = Column(String(255))

    def __str__(self):
        return self.qualifyId
    
    
class Race(db.Model):
    __tablename__ = 'races'
    raceId = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, ForeignKey('seasons.year', ondelete="CASCADE"), nullable=False, default=0)
    round = Column(Integer, nullable=False, default=0)
    circuitId = Column(Integer, ForeignKey('circuits.circuitId', ondelete="CASCADE"), nullable=False, default=0)
    name = Column(String(255), nullable=False)
    date = Column(Date, nullable=False, default='0000-00-00')
    time = Column(Time)
    url = Column(String(255))
    fp1_date = Column(Date)
    fp1_time = Column(Time)
    fp2_date = Column(Date)
    fp2_time = Column(Time)
    fp3_date = Column(Date)
    fp3_time = Column(Time)
    quali_date = Column(Date)
    quali_time = Column(Time)
    sprint_date = Column(Date)
    sprint_time = Column(Time)

    def __str__(self):
        return self.name
    
    
class Result(db.Model):
    __tablename__ = 'results'
    resultId = Column(Integer, primary_key=True, autoincrement=True)
    raceId = Column(Integer, ForeignKey('races.raceId', ondelete="CASCADE"), nullable=False, default=0)
    driverId = Column(Integer, ForeignKey('drivers.driverId', ondelete="CASCADE"), nullable=False, default=0)
    constructorId = Column(Integer, ForeignKey('constructors.constructorId', ondelete="CASCADE"), nullable=False, default=0)
    number = Column(Integer)
    grid = Column(Integer, nullable=False, default=0)
    position = Column(Integer)
    positionText = Column(String(255), nullable=False)
    positionOrder = Column(Integer, nullable=False, default=0)
    points = Column(Integer, nullable=False, default=0)
    laps = Column(Integer, nullable=False, default=0)
    time = Column(String(255))
    milliseconds = Column(Integer)
    fastestLap = Column(Integer)
    rank = Column(Integer, default=0)
    fastestLapTime = Column(Integer)
    fastestLapSpeed = Column(Integer)
    statusId = Column(Integer, ForeignKey('status.statusId', ondelete="CASCADE"), nullable=False, default=0)

    def __str__(self):
        return self.resultId
    
    
class SprintResult(db.Model):
    __tablename__ = 'sprintresults'
    sprintResultId = Column(Integer, primary_key=True, autoincrement=True)
    raceId = Column(Integer, ForeignKey('races.raceId', ondelete="CASCADE"), nullable=False, default=0)
    driverId = Column(Integer, ForeignKey('drivers.driverId', ondelete="CASCADE"), nullable=False, default=0)
    constructorId = Column(Integer, ForeignKey('constructors.constructorId', ondelete="CASCADE"), nullable=False, default=0)
    number = Column(Integer)
    grid = Column(Integer, nullable=False, default=0)
    position = Column(Integer)
    positionText = Column(String(255), nullable=False)
    positionOrder = Column(Integer, nullable=False, default=0)
    points = Column(Integer, nullable=False, default=0)
    laps = Column(Integer, nullable=False, default=0)
    time = Column(String(255))
    milliseconds = Column(Integer)
    fastestLap = Column(Integer)
    fastestLapTime = Column(Integer)
    statusId = Column(Integer, ForeignKey('status.statusId', ondelete="CASCADE"), nullable=False, default=0)

    def __str__(self):
        return self.sprintResultId
    
    
class Season(db.Model):
    __tablename__ = 'seasons'
    year = Column(Integer, primary_key=True)
    url = Column(String(255))

    def __str__(self):
        return self.year
    
    
class Status(db.Model):
    __tablename__ = 'status'
    statusId = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(255))

    def __str__(self):
        return self.status