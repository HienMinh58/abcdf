from recipe.adapters.datareader.csvdatareader import CSVDataReader

from recipe.domainmodel.user import User
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.review import Review
from recipe.domainmodel.favourite import Favourite


class MemoryRepository:
    def __init__(self):
        self._users = []
        self._recipes = []
        self._reviews = []
        self._favourites = []
        self.read_all_recipes('recipe/adapters/data/recipes.csv')
    
    def add_user(self, user : User):
        self._users.append(user)
    
    def add_recipe(self, recipe : Recipe):
        self._recipes.append(recipe)
    
    def get_recipe(self, recipe_id : int):
        return next((r for r in self._recipes if r.id == recipe_id), None)

    def read_all_recipes(self, csv_path : str):
        reader = CSVDataReader(csv_path)
        reader.csv_reader()
        self._recipes = reader.recipes

    def get_all_recipes(self):
        return list(self._recipes)

    def add_review(self, review : Review):
        self._reviews.append(review)
    
    def get_reviews_for_recipe(self, recipe_id : int):
        return [r for r in self._recipes if r.id == recipe_id]
    
    def add_favourite(self, favourite : Favourite):
        self._favourites.append(favourite)

    def get_favourites_for_user(self, user_id : int):
        return [f for f in self._favourites if f.user.id == user_id]


