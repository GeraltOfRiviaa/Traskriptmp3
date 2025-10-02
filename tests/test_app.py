import os

from app import create_app


def test_index_route():
    app = create_app("./tmp_uploads_test")
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Transkripce MP3" in resp.data
