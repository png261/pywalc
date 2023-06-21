from pywalc import pywal_util

from tests import CLIENT


def test_get_theme_list():
    response = CLIENT.get("/theme")
    assert response.status_code == 200
    assert response.json() == pywal_util.get_theme_list()


def test_get_theme():
    response = CLIENT.get("/theme/light/base16-tomorrow")
    assert response.status_code == 200
    assert (
        response.json()
        == pywal_util.get_theme("light", "base16-tomorrow")["colors"]
    )
