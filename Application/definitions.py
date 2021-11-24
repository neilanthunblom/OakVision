import os
import pathlib
ROOT_DIR = str(pathlib.Path(__file__).parent.absolute())


#ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH = os.path.join(ROOT_DIR, 'configuration.conf')
