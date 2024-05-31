from flask_wtf import FlaskForm
from wtforms import (
    FieldList,
    FormField,
    StringField,
    FloatField,
    TextAreaField,
    SelectMultipleField,
    IntegerField,
    HiddenField,
)
from wtforms.validators import DataRequired, Length
from .photo import UploadPhotoForm


class RecipeIngredientForm(FlaskForm):
    recipe_uuid = HiddenField("Recipe UUID", [DataRequired()])
    plant_uuid = StringField(
        "Plant UUID",
        [DataRequired()],
        render_kw={"placeholder": "Select ingredient", "autocomplete": "off"},
    )
    quantity = FloatField("Quantity", [DataRequired()], render_kw={"placeholder": "200"})
    quantity_type = StringField("Quantity Type", [DataRequired()], render_kw={"placeholder": "Grams"})


class RecipeAdditionalIngredientForm(FlaskForm):
    uuid = HiddenField()
    additional_ingredient = StringField(
        "Additional Ingredients",
        [DataRequired()],
        render_kw={"placeholder": "Select ingredient", "autocomplete": "off"},
    )
    text_quantity = StringField("Text quantity", [DataRequired()], render_kw={"placeholder": "Pinch"})


class RecipeForm(UploadPhotoForm, FlaskForm):
    name = StringField("Name", [DataRequired(), Length(1, 64)], render_kw={"placeholder": "Enter name"})
    cooking_time = IntegerField("Cooking Time", [DataRequired()], render_kw={"placeholder": "Enter cooking time"})
    description = TextAreaField("Description", [DataRequired()], render_kw={"placeholder": "Enter description"})
    categories = SelectMultipleField("Categories", choices=[])
    additional_ingredients = FieldList(FormField(RecipeAdditionalIngredientForm))
