from sqlalchemy.orm import Session

import app.schema as s
import app.models as m


def init_fake_data(session: Session, fake_data: s.TestData):
    for test_user in fake_data.test_users:
        user = m.User(
            username=test_user.username,
            email=test_user.email,
            password=test_user.password,
        )
        session.add(user)
    for category in fake_data.categories:
        session.add(m.PlantCategory(**category.model_dump()))
    categories = []
    for recipe_category in fake_data.recipe_categories:
        category = m.Category(**recipe_category.model_dump())
        session.add(category)
        categories.append(category)

    recipes = []
    for recipe in fake_data.recipes:
        recipe = m.Recipe(**recipe.model_dump())
        recipe.categories = categories
        session.add(recipe)
        recipes.append(recipe)

    plant_varieties = []
    for plant_family in fake_data.plant_families:
        session.add(m.PlantFamily(**plant_family.model_dump()))
    for plant_variety in fake_data.plant_varieties:
        plant_variety = m.PlantVariety(**plant_variety.model_dump())
        session.add(plant_variety)
        plant_varieties.append(plant_variety)
    for step_type in fake_data.planting_step_types:
        session.add(m.PlantingStepType(**step_type.model_dump(), color="red"))

    session.commit()
    for plant_variety in plant_varieties:
        ingredients = m.RecipeIngredient(
            recipe_id=recipes[0].id,
            quantity=1,
            quantity_type="kg",
            plant_variety_id=plant_variety.id,
        )
        session.add(ingredients)
    session.commit()
