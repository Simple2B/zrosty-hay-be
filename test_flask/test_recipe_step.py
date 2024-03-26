from flask.testing import FlaskClient
from .db import FakeData
import sqlalchemy as sa


from app import models as m, db


def test_CRU(login_client: FlaskClient, add_fake_data: FakeData):
    recipe = m.Recipe(
        name="Need sun",
        cooking_time=3600,
        additional_ingredients="water",
        description="test",
    )
    recipe.save()

    res = login_client.get(f"/recipes-step/{recipe.uuid}/step-form")
    assert res.status_code == 200
    assert recipe.uuid.encode("utf-8") in res.data  # type: ignore
    form_data = {
        "name": "Step 1",
        "step_number": 1,
        "instruction": "Test",
        "recipe_uuid": recipe.uuid,
    }
    res = login_client.post("/recipes-step/add-step", data=form_data)
    assert res.status_code == 200
    assert b"Step 1" in res.data

    step = db.session.scalar(sa.select(m.RecipeStep).where(m.RecipeStep.name == "Step 1"))

    res = login_client.get(f"/recipes-step/{step.uuid}/edit")
    assert res.status_code == 200
    assert recipe.uuid.encode("utf-8") in res.data
    assert b"Step 1" in res.data
    form_data = {
        "name": "Step 2",
        "step_number": 2,
        "instruction": "Test",
        "recipe_uuid": recipe.uuid,
    }
    res = login_client.post(f"/recipes-step/{step.uuid}/edit", data=form_data)
    assert res.status_code == 200
    assert b"Step 2" in res.data

    res = login_client.delete(f"/recipes-step/{step.uuid}")
    assert res.status_code == 200

    db.session.refresh(recipe)
    assert not recipe.steps
