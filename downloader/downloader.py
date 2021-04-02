import os
from shutil import rmtree
import urllib.request

from map.osm_loader import MapLoader
from map.map import Map

# https://overpass-api.de/api/map?bbox=18.1566,49.8296,18.1662,49.8373


class Downloader:

    tmp_folder = '.downloader'
    top_key = 'MAP_BOUNDARY_TOP'
    bottom_key = 'MAP_BOUNDARY_BOTTOM'
    left_key = 'MAP_BOUNDARY_LEFT'
    right_key = 'MAP_BOUNDARY_RIGHT'

    pretty_out_key = 'PRETTIFY'

    def __init__(self):
        try:
            self.top = float(os.environ[Downloader.top_key])
            self.bottom = float(os.environ[Downloader.bottom_key])
            self.left = float(os.environ[Downloader.left_key])
            self.right = float(os.environ[Downloader.right_key])

            prettify = os.environ.get(Downloader.pretty_out_key, '0')
            if not prettify.isdigit():
                raise RuntimeError(f"Value of '{Downloader.pretty_out_key}' must be numeric")
            self.prettify = bool(int(prettify))
        except:
            raise RuntimeError('Invalid configuration')

    @property
    def api_url(self) -> str:
        return f'https://overpass-api.de/api/map?bbox={self.left},{self.bottom},{self.right},{self.top}'

    @property
    def osm_file(self) -> str:
        return f'{Downloader.tmp_folder}/map.xml'

    @property
    def out_file(self):
        return 'map.json'

    @staticmethod
    def create_tmp_folder():
        os.mkdir(Downloader.tmp_folder)

    @staticmethod
    def delete_tmp_folder():
        if os.path.exists(Downloader.tmp_folder):
            rmtree(Downloader.tmp_folder)

    def cleanup(self):
        Downloader.delete_tmp_folder()

    def download(self):
        urllib.request.urlretrieve(self.api_url, self.osm_file)

    def store(self, m: Map):
        json = m.to_json(pretty=self.prettify)

        with open(self.out_file, 'w') as f:
            f.write(json)
            f.write('\n')  # Ensure newline at EOF

    def process(self):
        m = MapLoader.load(self.osm_file)
        self.store(m)

    def run(self):
        Downloader.delete_tmp_folder()
        Downloader.create_tmp_folder()

        self.download()
        self.process()
        self.cleanup()

