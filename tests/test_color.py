from pywalc import util
from pywalc.settings import PYWAL_DATA_FILE

from tests import CLIENT


def test_get_color():
    response = CLIENT.get("/color")
    assert response.status_code == 200
    assert response.json() == util.read_file_json(PYWAL_DATA_FILE)["colors"]


def test_update_color():
    response = CLIENT.get("/color")
    assert response.status_code == 200
    assert response.json() == util.read_file_json(PYWAL_DATA_FILE)["colors"]
    colors = response.json()
    colors["color0"] = "#FFFFFF"

    response = CLIENT.put("/color", json=colors)
    assert response.status_code == 200
    assert response.json() == colors


def test_apply_color():
    response = CLIENT.get("/color/apply")
    assert response.status_code == 200
    test_get_color()
