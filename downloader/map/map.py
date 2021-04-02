from typing import Set, Union
import json

from map.node import Node
from map.path import Path


class Map:
    def __init__(self):
        self.nodes: Set[Node] = set()
        self.paths: Set[Path] = set()

    def add_node(self, node: Node) -> None:
        if node in self.nodes:
            return

        self.nodes.add(node)

    def add_path(self, path: Path) -> None:
        if path in self.paths or path.reverse() in self.paths:
            return

        self.paths.add(path)

        for node in self.nodes:
            node.add_path(path)

    def add(self, item: Union[Path, Node]) -> None:
        if type(item) is Path:
            self.add_path(item)
        elif type(item) is Node:
            self.add_node(item)

    def reduce(self) -> None:
        filtered = filter(lambda node: len(node.paths) > 0, self.nodes)
        self.nodes = set(filtered)

    def to_json(self, pretty: bool = False) -> str:
        nodes = [node.json_dict for node in self.nodes]
        paths = [path.json_dict for path in self.paths]
        map_dict = {
            'nodes': nodes,
            'paths': paths
        }
        outer_dict = {'map': map_dict}
        return json.dumps(outer_dict, indent=2) if pretty else json.dumps(outer_dict)
