from flask import Blueprint, render_template, request
from flask_paginate import Pagination, get_page_parameter
from recipe.adapters.datareader.csvdatareader import CSVDataReader

reader = CSVDataReader('recipe/adapters/data/recipes.csv')
reader.csv_reader()

browse_bp = Blueprint('browse', __name__)

@browse_bp.route('/browse')
def browse():
    all_recipes = reader.recipes
    sort_by = request.args.get('sort', 'name')
    # if sort_by == 'name':
    #     all_recipes.sort(key=lambda r: r.name.lower())
    # elif sort_by =='cooking_time':
    #     all_recipes.sort(key=lambda r: r.created_date.)
    all_recipes.sort(key=lambda r: r.name.lower())
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10
    offset = (page - 1) * per_page
    paginated_recipes = all_recipes[offset:offset + per_page]

    pagination = Pagination(page=page, total=len(all_recipes), per_page=per_page, css_framework='bootstrap5')
    return render_template('browse.html', recipes=paginated_recipes, pagination=pagination)