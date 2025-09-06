from flask import Blueprint, render_template, request
from recipe.adapters.datareader.csvdatareader import CSVDataReader
from recipe.adapters.memory_repo import MemoryRepository

recipe_details_bp = Blueprint('recipe_details', __name__, template_folder='../templates')
repo = MemoryRepository()

@recipe_details_bp.route('/recipe_details/<int:recipe_id>')
def display_recipe(recipe_id):
    recipe = repo.get_recipe(recipe_id)
    if recipe is None:
        return "Recipe not found", 404
    
    back_url = request.referrer or '/browse'

    ingredient_pairs = zip(recipe.ingredient_quantities, recipe.ingredients)
    return render_template('recipe.html', recipe=recipe, ingredient_pairs=ingredient_pairs, back_url=back_url)