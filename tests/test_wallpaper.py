import os
import random
from pywalc import util
from pywalc.settings import WALLPAPER_DIR as PYWALLC_WALLPAPER_DIR

from tests import CLIENT, TEST_FILES_DIR


def test_get_wallpaper():
    response = CLIENT.get("/wallpaper")
    assert response.status_code == 200
    data = response.json()
    assert data["current"] == "current"
    assert data["list"] == os.listdir(PYWALLC_WALLPAPER_DIR)


def test_get_wallpaper_color():
    images = ["image_1.png", "image_2.png"]
    files = [
        ("files", open(os.path.join(TEST_FILES_DIR, image), "rb"))
        for image in images
    ]

    response = CLIENT.post("/wallpaper", files=files)
    assert response.status_code == 200
    assert len(response.json()) == 2
    list_id = response.json()

    response = CLIENT.get(f"/wallpaper/{list_id[0]}/color")
    assert response.status_code == 200
    assert response.json() == util.read_file_json(
        os.path.join(TEST_FILES_DIR, "image_1_colors.json")
    )

    response = CLIENT.get(f"/wallpaper/{list_id[1]}/color")
    assert response.status_code == 200
    assert response.json() == util.read_file_json(
        os.path.join(TEST_FILES_DIR, "image_2_colors.json")
    )


def test_upload_wallpaper():
    images = ["image_1.png", "image_2.png"]
    files = [
        ("files", open(os.path.join(TEST_FILES_DIR, image), "rb"))
        for image in images
    ]

    response = CLIENT.post("/wallpaper", files=files)
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_set_wallpaper():
    random_wallpaper_id = random.choice(os.listdir(PYWALLC_WALLPAPER_DIR))
    response = CLIENT.put(f"/wallpaper/{random_wallpaper_id}")
    assert response.status_code == 200


def test_apply_wallpaper():
    response = CLIENT.get("/wallpaper/apply")
    assert response.status_code == 200
