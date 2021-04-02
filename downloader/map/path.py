from typing import Dict

from map.geo_position import GeoPosition


class Path:
    def __init__(self, begin: GeoPosition, end: GeoPosition):
        self.begin = begin
        self.end = end

    @property
    def json_dict(self) -> Dict[str, Dict[str, float]]:
        return {
            'begin': self.begin.__dict__,
            'end': self.end.__dict__
        }

    def reverse(self):
        return Path(begin=self.end, end=self.begin)

    def __hash__(self):
        return hash((self.begin, self.end))
