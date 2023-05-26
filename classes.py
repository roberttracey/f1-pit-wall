class RaceOrder:
    def __init__(self, lapnumber, driver, team, compound, tyrelife, time, gap, behind, trackstatus):
        self._lapnumber = lapnumber
        self._driver = driver
        self._team = team
        self._compound = compound
        self._time = time
        self._gap = gap
        self._behind = behind
        self._tyrelife = tyrelife
        self._trackstatus = trackstatus
       

    def __str__(self):
        return f"(lapnumber={self._lapnumber}, driver='{self._driver}', team='{self._team}', compound='{self._compound}', tyrelife='{self._tyrelife}', time={self._time}, gap={self._gap}, behind={self._behind}, trackstatus={self._trackstatus})"
    
    def as_dict(self):
        return {
            'lapnumber': self._lapnumber,
            'driver': self._driver,
            'team': self._team,
            'compound': self._compound,
            'tyrelife': self._tyrelife,
            'time': self._time,
            'gap': self._gap,
            'behind': self._behind,
            'trackstatus': self._trackstatus
        }
    
class Simulation:
    def __init__(self, lap, raceId, driver, interval):
        self._lap = lap
        self._raceId = raceId
        self._driver = driver
        self._interval = interval

    # getters
    def get_lap(self):
        return self._lap

    def get_raceId(self):
        return self._raceId
    
    def get_driver(self):
        return self._driver
    
    def get_interval(self):
        return self._interval


    # setters
    def set_lap(self, value):
        self._lap = value

    def set_raceId(self, value):
        self._raceId = value

    def set_driver(self, value):
        self._driver = value

    def set_interval(self, value):
        self._interval = value

    # increment Methods
    def incrementLap(self):
        self._lap += 1

class LapGraph:
    def __init__(self, lapnumber, driver, laptimes):
        self._lapnumber = lapnumber
        self._driver = driver
        self._laptimes = laptimes

    def __str__(self):
        return f"(lapnumber={self._lapnumber}, driver='{self._driver}', laptimes='{self._laptimes}')"
    
    def as_dict(self):
        return {
            'lapnumber': self._lapnumber,
            'driver': self._driver,
            'laptimes': self._laptimes
        }

    def add_time(self, laptime):   
        self._laptimes.append(laptime)

class Battle:
    def __init__(self, driver, s1Delta, s2Delta, s3Delta, lapDelta, gap, compound, tyrelife, drs):
        self._driver = driver
        self._s1Delta = s1Delta
        self._s2Delta = s2Delta
        self._s3Delta = s3Delta
        self._lapDelta = lapDelta
        self._gap = gap
        self._compound = compound
        self._tyrelife = tyrelife
        self._drs = drs

    def __str__(self):
        return f"(driver={self._driver}, s1Delta='{self._s1Delta}', s2Delta='{self._s2Delta}', s3Delta='{self._s3Delta}', lapDelta='{self._lapDelta}', gap='{self._gap}', compound='{self._compound}', tyrelife='{self._tyrelife}', drs='{self._drs}')"
    
    def as_dict(self):
        return {
            'driver': self._driver,
            's1Delta': self._s1Delta,
            's2Delta': self._s2Delta,
            's3Delta': self._s3Delta,
            'lapDelta': self._lapDelta,
            'gap': self._gap,
            'compound': self._compound,
            'tyrelife': self._tyrelife,
            'drs': self._drs
        }
    

class PitStopData:
    def __init__(self, driver, stop, lap, duration, milliseconds):
        self._driver = driver
        self._stop = stop
        self._lap = lap
        self._duration = duration
        self._milliseconds = milliseconds

    def __str__(self):
        return f"(driver={self._driver}, stop='{self._stop}', lap='{self._lap}', duration='{self._duration}', milliseconds='{self._milliseconds}')"
    
    def as_dict(self):
        return {
            'driver': self._driver,
            'stop': self._stop,
            'lap': self._lap,
            'duration': self._duration,
            'milliseconds': self._duration
        }