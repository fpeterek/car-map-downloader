from typing import Set, Dict

from geo_position import GeoPosition
from path import Path


class Node:
    def __init__(self, position: GeoPosition):
        self.paths: Set[Path] = set()
        self.position = position

    def add_path(self, path: Path) -> None:
        if path.begin != self.position and path.end != self.position:
            return

        if path in self.paths or path.reverse() in self.paths:
            return

        self.paths.add(path)

    @property
    def json_dict(self) -> dict[str, dict[str, float]]:
        return {'position': self.position.__dict__}

    def __hash__(self):
        return hash(self.position)
