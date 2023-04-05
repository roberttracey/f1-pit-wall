class RaceOrder:
    def __init__(self, lapnumber, driver, team, compound, time, gap, behind):
        self._lapnumber = lapnumber
        self._driver = driver
        self._team = team
        self._compound = compound
        self._time = time
        self._gap = gap
        self._behind = behind
       

    def __str__(self):
        return f"(lapnumber={self._lapnumber}, driver='{self._driver}', team='{self._team}', compound='{self._compound}', time={self._time}, gap={self._gap}, behind={self._behind})"
    
    def as_dict(self):
        return {
            'lapnumber': self._lapnumber,
            'driver': self._driver,
            'team': self._team,
            'compound': self._compound,
            'time': self._time,
            'gap': self._gap,
            'behind': self._behind
        }
    
class Race:
    def __init__(self, lap, raceId, time):
        self._lap = lap
        self._raceId = raceId
        self._time = time

    # getters
    @property
    def lap(self):
        return self._lap

    @property
    def raceId(self):
        return self._raceId

    @property
    def time(self):
        return self._time

    # setters
    @lap.setter
    def lap(self, value):
        self._lap = value

    @raceId.setter
    def raceId(self, value):
        self._raceId = value

    @time.setter
    def time(self, value):
        self._time = value

    # increment Methods
    def incrementLap(self):
        self._lap += 1

    def incrementTime(self, increment):
        self._time += increment