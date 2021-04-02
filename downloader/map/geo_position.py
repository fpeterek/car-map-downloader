
class GeoPosition:
    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon

    def __hash__(self):
        return hash((self.lat, self.lon))

    def __eq__(self, other) -> bool:
        if type(other) is not GeoPosition:
            return False
        return self.lat == other.lat and self.lon == other.lon

    def __ne__(self, other):
        return not (self == other)
