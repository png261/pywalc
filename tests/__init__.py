import os
from fastapi.testclient import TestClient

from pywalc.server import Server
from pywalc.app import App

App().setup()
SERVER = Server(2601)
SERVER.setup()
CLIENT = TestClient(SERVER.server)

CURRENT_DIR = os.path.dirname(__file__)
TEST_FILES_DIR = os.path.join(CURRENT_DIR, "test_files")
