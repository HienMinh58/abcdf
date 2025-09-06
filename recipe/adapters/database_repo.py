# import sqlite3 
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
# from recipe.adapters.datareader.csvdatareader import CSVDataReader



# csv = CSVDataReader('recipe/adapters/data/recipes.csv')
# file_path = csv.csv_path
# db_path = 'recipe/adapters/data/database.db'
# sql_file = 'recipe/adapters/data/database.sql'
    
# def csv_to_sql(file_path, db_path, sql_file):
#     csv.csv_reader()
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()
    
#     recipes = csv.recipes
#     authors = csv.authors
#     category = csv.categories
#     for i, recipe in enumerate(recipes[:5], 1):
#         print(f"recipe {i}")
#         for attr, value in vars(recipe).items():
#             print(f"{attr} : {value}")
    
#     for i, recipe in enumerate(recipes):
#         cursor.execute(
#             "INSERT INTO recipes (name, ingredients, instructions, cooking_time, category_id, author_id, nutrition_info) VALUES (?)", 
#             (recipe.name), (recipe.ingredients), (recipe.instructions), (recipe.cook_time), (recipe.category_id), (authors[i].id), (category[i].id), (recipe.nutrition)
#             "INSERT INTO category (name) VALUES (?)", (category[i].name)
#             )

        
# if __name__ == "__main__":
#     csv_to_sql(file_path=file_path, db_path=db_path, sql_file=sql_file)


import sqlite3

class DatabaseRepository:
    def __init__(self, db_path='recipe/adapters/data/database.db'):
        self.db_path = db_path
        self.init_db()
        
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            with open('recipe/adapters/data/database.sql', 'r') as sql_file:
                cursor.executescript(sql_file.read())
            conn.commit()
            print("Database schema initialized successfully.")
        except sqlite3.Error as e:
            print(f"Error initializing database: {e}")
        finally:
            conn.close()
            
    def add_categories(self, categories):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            for category_name in categories.keys():
                cursor.execute("INSERT OR IGNORE INTO category (name) VALUES (?)", (category_name,))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error inserting categories: {e}")
        finally:
            conn.close()
                
    def add_authors(self, authors):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            author_data = [(author.name,) for author in authors.values()]
            cursor.executemany("INSERT OR IGNORE INTO authors (name) VALUES (?)", author_data)
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error inserting authors: {e}")
        finally:
            conn.close()
            
    def add_recipes(self, recipes):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT name, id FROM category")
            category_map = {name: id for name, id in cursor.fetchall()}
            
            cursor.execute("SELECT name, id FROM authors")
            author_map = {name: id for name, id in cursor.fetchall()}
            recipe_data = []
            for recipe in recipes:
                ingredients = ", ".join(recipe.ingredients) if isinstance(recipe.ingredients, list) else recipe.ingredients
                instructions = ", ".join(recipe.instructions) if isinstance(recipe.instructions, list) else recipe.instructions
                
                if isinstance(recipe.nutrition, str):
                    nutrition = recipe.nutrition
                else:
                    nutrition_attrs = vars(recipe.nutrition)
                    nutrition = ", ".join(f"{key.replace('_Nutrition__', '')}: {value}"
                                         for key, value in nutrition_attrs.items()
                                         if key != '_Nutrition__id') or str(recipe.nutrition)
                category_name = recipe.category.name
                author_name = recipe.author.name
                category_id = category_map.get(category_name)
                author_id = author_map.get(author_name)
            
                recipe_data.append((recipe.name, ingredients, instructions, recipe.cook_time, 
                                  category_id, author_id, nutrition))
            
            if recipe_data:
                cursor.executemany("""
                    INSERT INTO recipes (name, ingredients, instructions, cooking_time, category_id, author_id, nutrition_info)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, recipe_data)
                conn.commit()
                print(f"Inserted {len(recipe_data)} recipes.")
        except sqlite3.Error as e:
            print(f"Error inserting recipes: {e}")
        finally:
            conn.close()
        #     for i, recipe in enumerate(recipes):
        #         ingredients = ", ".join(recipe.ingredients) if isinstance(recipe.ingredients, list) else recipe.ingredients
        #         instructions = ", ".join(recipe.instructions) if isinstance(recipe.instructions, list) else recipe.instructions
        #         if isinstance(recipe.nutrition, str):
        #             nutrition = recipe.nutrition
        #         else:
        #             nutrition_attrs = vars(recipe.nutrition)
        #             nutrition = ", ".join(f"{key.replace('_Nutrition__', '')}: {value}"
        #                                   for key, value in nutrition_attrs.items()
        #                                   if key != '_Nutrition__id') or str(recipe.nutrition)
        #         cursor.execute("""
        #                        INSERT INTO recipes (name, ingredients, instructions, cooking_time, category_id, author_id, nutrition_info)
        #                        VALUES (?, ?, ?, ?, ?, ?, ?)
        #                        """, (recipe.name, ingredients, instructions, recipe.cook_time, 
        #                             recipe.category.id, recipe.author.id, nutrition))
        #         conn.commit()
        # except sqlite3.Error as e:
        #     print(f"Error inserting recipes: {e}")
        # finally:
        #     conn.close()
    
    def load_data(self, categories, authors, recipes):
        self.add_categories(categories)
        self.add_authors(authors)
        self.add_recipes(recipes)
        print("Data loaded successfully.")
        
    def print_first_five_recipes(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT name, ingredients, instructions, cooking_time FROM recipes LIMIT 5")
            recipes = cursor.fetchall()
            for i, recipe in enumerate(recipes, 1):
                print(f"Recipe {i}:")
                print(f"  Name: {recipe[0]}")
                print(f"  Ingredients: {recipe[1]}")
                print(f"  Instructions: {recipe[2]}")
                print(f"  Cooking Time: {recipe[3]} minutes")
                print()
        except sqlite3.Error as e:
            print(f"Error retrieving recipes: {e}")
        finally:
            conn.close()
    
    def clear_data(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM recipes")
            cursor.execute("DELETE FROM category")
            cursor.execute("DELETE FROM authors")
            conn.commit()
            print("All data cleared from database successfully")
        except sqlite3.Error as e:
            print(f"Error clearing data: {e}")
        finally:
            conn.close()
            
if __name__ == "__main__":
    db = DatabaseRepository()
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    from recipe.adapters.datareader.csvdatareader import CSVDataReader 
    
    csv = CSVDataReader('recipe/adapters/data/recipes.csv')
    
    csv.csv_reader()
    recipes = csv.recipes
    authors = csv.authors
    categories = csv.categories
    
    

    
    # for recipe in recipes[:5]:
    #     print("Nutrition type:", type(recipe.nutrition))
    #     print("Nutrition vars:", vars(recipe.nutrition))
    # print("Type of categories:", type(categories))
    # print("Content of categories:", categories)
    print("Type of categories:", type(categories))
    print("Content of categories:", categories)
    print("Type of authors:", type(authors))
    print("Content of authors:", authors)
    db.clear_data()
    db.load_data(categories=categories, authors=authors, recipes=recipes)
    db.print_first_five_recipes()
    # db.clear_data()
    
        