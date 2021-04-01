
class GeoPosition:
    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon

    def __hash__(self):
        return hash((self.lat, self.lon))
