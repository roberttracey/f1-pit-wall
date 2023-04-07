class RaceOrder:
    def __init__(self, lapnumber, driver, team, compound, tyrelife, time, gap, behind):
        self._lapnumber = lapnumber
        self._driver = driver
        self._team = team
        self._compound = compound
        self._time = time
        self._gap = gap
        self._behind = behind
        self._tyrelife = tyrelife
       

    def __str__(self):
        return f"(lapnumber={self._lapnumber}, driver='{self._driver}', team='{self._team}', compound='{self._compound}', tyrelife='{self._tyrelife}', time={self._time}, gap={self._gap}, behind={self._behind})"
    
    def as_dict(self):
        return {
            'lapnumber': self._lapnumber,
            'driver': self._driver,
            'team': self._team,
            'compound': self._compound,
            'tyrelife': self._tyrelife,
            'time': self._time,
            'gap': self._gap,
            'behind': self._behind
        }
    
class Simulation:
    def __init__(self, lap, raceId, driver):
        self._lap = lap
        self._raceId = raceId
        self._driver = driver

    # getters
    @property
    def lap(self):
        return self._lap

    @property
    def raceId(self):
        return self._raceId
    
    @property
    def driver(self):
        return self._driver

    # setters
    @lap.setter
    def lap(self, value):
        self._lap = value

    @raceId.setter
    def raceId(self, value):
        self._raceId = value

    @driver.setter
    def driver(self, value):
        self._driver = value

    # increment Methods
    def incrementLap(self):
        self._lap += 1