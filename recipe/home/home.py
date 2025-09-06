import random
from flask import Blueprint, render_template
#from recipe.adapters.datareader.csvdatareader import CSVDataReader
from recipe.adapters.memory_repo import MemoryRepository

#reader = CSVDataReader('recipe/adapters/data/recipes.csv')
#reader.csv_reader()
#all_recipes = reader.recipes

home_bp = Blueprint('home', __name__)
repo = MemoryRepository()

@home_bp.route('/')
def home():
    all_recipes = repo.get_all_recipes()
    featured_recipes = random.sample(all_recipes, k=4)
    return render_template('home.html', recipes=featured_recipes)