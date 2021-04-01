import osmium

from map.map import Map
from node import Node
from geo_position import GeoPosition
from path import Path


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

        for i in range(1, len(way.nodes)):
            current = way.nodes[i]

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
