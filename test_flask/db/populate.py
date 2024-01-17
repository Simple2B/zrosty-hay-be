from typing import Generator
from faker import Faker
from sqlalchemy import func
from app import db
from app import models as m

faker = Faker()

NUM_TEST_USERS = 100


def gen_test_items(num_objects: int) -> Generator[tuple[str, str], None, None]:
    from faker import Faker

    fake = Faker()

    DOMAINS = ("com", "com.br", "net", "net.br", "org", "org.br", "gov", "gov.br")

    i = db.session.query(func.max(m.User.id)).scalar()

    for _ in range(num_objects):
        i += 1
        # Primary name
        first_name = fake.first_name()

        # Secondary name
        last_name = fake.last_name()

        company = fake.company().split()[0].strip(",")

        # Company DNS
        dns_org = fake.random_choices(elements=DOMAINS, length=1)[0]

        # email formatting
        yield f"{first_name}{i}".lower(), f"{first_name}.{last_name}{i}@{company}.{dns_org}".lower()


def populate(count: int = NUM_TEST_USERS):
    for username, email in gen_test_items(count):
        m.User(
            username=username,
            email=email,
        ).save(False)

    db.session.commit()


def get_pests() -> list[m.Pest]:
    pests = db.session.scalars(m.Pest.select().limit(10)).all()
    if pests:
        return pests
    for index in range(10):
        pest = m.Pest(
            name=f"Pest_{index}",
            symptoms=f"Symptoms_{index}",
            treatment=f"Treatment_{index}",
        )
        db.session.add(pest)
        pests.append(pest)
    db.session.commit()
    return pests


def get_illnesses() -> list[m.Illness]:
    illnesses = db.session.scalars(m.Illness.select().limit(10)).all()
    if illnesses:
        return illnesses
    for index in range(10):
        illness = m.Illness(
            name=f"Illness_{index}",
            reason=f"Reason_{index}",
            symptoms=f"Symptoms_{index}",
            treatment=f"Treatment_{index}",
        )
        db.session.add(illness)
        illnesses.append(illness)
    db.session.commit()
    return illnesses


def get_plant_families() -> list[m.PlantFamily]:
    plant_families = db.session.scalars(m.PlantFamily.select().limit(10)).all()
    if plant_families:
        return plant_families
    pests = get_pests()
    illnesses = get_illnesses()
    for index in range(10):
        plant_family = m.PlantFamily(
            name=f"PlantFamily_{index}",
            features=f"Features_{index}",
            type_of=m.PlantFamilyType.vegetable.value,
        )
        db.session.add(plant_family)
        plant_families.append(plant_family)
        plant_family.pests.extend(faker.random_choices(elements=pests, length=3))
        plant_family.illnesses.extend(faker.random_choices(elements=illnesses, length=3))
    db.session.commit()
    return plant_families


def create_plant_varieties() -> list[m.PlantFamily]:
    plant_families = get_plant_families()
    pests = get_pests()
    illnesses = get_illnesses()
    plant_varieties = []
    for index in range(10):
        plant_variety = m.PlantVariety(
            name=f"PlantVariety_{index}",
            plant_family_id=faker.random_choices(elements=plant_families, length=1)[0].id,
        )
        db.session.add(plant_variety)
        plant_variety.pests.extend(faker.random_choices(elements=pests, length=3))
        plant_variety.illnesses.extend(faker.random_choices(elements=illnesses, length=3))
        plant_varieties.append(plant_variety)
    db.session.commit()
    return plant_varieties
