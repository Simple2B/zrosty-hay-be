from flask.testing import FlaskClient
from app import models as m, db


def test_delete_photo(login_client: FlaskClient):
    photo = m.Photo(url_path="test", original_name="test")
    photo.save()
    assert not photo.is_deleted

    res = login_client.delete(f"/photos/{photo.uuid}")
    assert res.status_code == 200
    db.session.refresh(photo)
    assert photo.is_deleted
