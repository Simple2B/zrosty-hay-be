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

    # test get_modal_add_ingredient
    res = login_client.get(f"/recipes/{recipe.uuid}/add-ingredient")
    assert res.status_code == 200

    # test add_ingredient
    assert not recipe.ingredients
    form_data = dict(
        recipe_uuid=recipe.uuid,
        plant_uuid=plant_variety.uuid,
        quantity=1,
        quantity_type="kg",
    )
    res = login_client.post("/recipes/add-ingredient", data=form_data, follow_redirects=True)
    assert res.status_code == 200

    assert recipe.ingredients

    assert plant_variety.recipes[0].name == recipe.name

    # delete ingredient
    res = login_client.delete(f"/recipe-ingredient/{recipe.ingredients[0].uuid}")
    assert res.status_code == 200

    assert not recipe.ingredients
    assert not plant_variety.recipes
