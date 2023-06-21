import platform
import socket

from tests import CLIENT


def test_get_home():
    response = CLIENT.get("/")
    assert response.status_code == 200


def test_get_system_info():
    response = CLIENT.get("/sys")
    assert response.status_code == 200
    assert response.json()["os"] == platform.uname()[0]
    assert response.json()["name"] == socket.gethostname()
