from flask_wtf import FlaskForm
from wtforms import FieldList, FormField, StringField, TextAreaField, SelectMultipleField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Length
from .photo import UploadPhotoForm


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


class RecipeIngredientForm(FlaskForm):
    ingredient = StringField(
        "Ingredients",
        [DataRequired()],
        render_kw={"placeholder": "Select ingredient", "autocomplete": "off"},
    )
    text_quantity = StringField("Text quantity", [DataRequired()], render_kw={"placeholder": "Pinch"})
    unit = StringField("Unit", [DataRequired()], render_kw={"placeholder": "g"})
    quantity = IntegerField("Quantity", [DataRequired()], render_kw={"placeholder": "10"})
