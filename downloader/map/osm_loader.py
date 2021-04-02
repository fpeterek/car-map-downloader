import osmium

from map.map import Map
from map.node import Node
from map.geo_position import GeoPosition
from map.path import Path


class MapLoaderHandler(osmium.SimpleHandler):
    excluded_ways = ('footway', 'corridor', 'sidewalks', 'steps', 'crossing')

    def __init__(self):
        super(MapLoaderHandler, self).__init__()
        self.map = Map()

    def node(self, n):
        position = GeoPosition(lon=n.location.lon, lat=n.location.lat)
        node = Node(position=position)
        self.map.add(node)

    def way(self, way):
        if not way.nodes or 'highway' not in way.tags or way.is_closed():
            return
        if way.tags['highway'] in MapLoaderHandler.excluded_ways:
            return
        previous = way.nodes[0]
        # Ensure nodes are added to map in case they haven't been added before
        # We want nodes to be added before ways, not the other way around
        # Adding all necessary nodes here helps ensure that
        self.map.add(previous)

        for i in range(1, len(way.nodes)):
            current = way.nodes[i]
            self.map.add(current)

            begin = GeoPosition(lon=previous.lon, lat=previous.lat)
            end = GeoPosition(lon=current.lon, lat=current.lat)

            path = Path(begin=begin, end=end)
            self.map.add(path)

            previous = current

    def relation(self, way):
        """noop -> There's no need to handle relations, at least not now"""


class MapLoader:
    def __init__(self):
        pass

    @staticmethod
    def load(path: str) -> Map:
        handler = MapLoaderHandler()
        handler.apply_file(path, locations=True)
        handler.map.reduce()
        return handler.map
