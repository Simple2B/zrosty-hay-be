from flask.testing import FlaskClient
from .db import FakeData


from app import models as m, db


def test_CRU(login_client: FlaskClient, add_fake_data: FakeData):
    category = m.Category(name="test").save()
    plant_variety: m.PlantVariety = add_fake_data.plant_varieties[0]
    form_data = dict(
        name="Need sun",
        cooking_time=3600,
        additional_ingredients="water",
        description="test",
        categories=[category.name],
        plant_varieties=[plant_variety.name],
    )

    res = login_client.post("/recipes/add", data=form_data, follow_redirects=True)
    assert res.status_code == 200
    assert form_data["name"].encode("utf-8") in res.data  # type: ignore
    recipe = db.session.get(m.Recipe, 1)
    assert recipe
    assert recipe.name == form_data["name"]

    form_data["name"] = "new name"
    plant_variety: m.PlantVariety = add_fake_data.plant_varieties[1]  # type: ignore
    form_data["plant_varieties"] = [plant_variety.name]
    res = login_client.post(f"/recipes/{recipe.uuid}/edit", data=form_data, follow_redirects=True)
    assert res.status_code == 200
    db.session.refresh(recipe)
    assert recipe.name == form_data["name"]
    assert recipe.plant_varieties[0].name == plant_variety.name
