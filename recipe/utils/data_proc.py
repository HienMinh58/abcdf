import sqlite3
import json
import sys
import os
import torch
import numpy as np

from sentence_transformers import SentenceTransformer, util


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

model = SentenceTransformer('all-MiniLM-L6-v2')

db_path = 'recipe/adapters/data/database.db'

def sample(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name, ingredients, instructions, cooking_time FROM recipes LIMIT 5")
    recipes = cursor.fetchall()
    
    json_string = []
    
    for i, recipe in enumerate(recipes):
        json_string.append({
            "Recipe name": recipe[0],
            "Ingredients": recipe[1],
            "Instructions": recipe[2],
            "Cooking time": f"{recipe[3]} minutes"
        })
    
    json_string = json.dumps(json_string, indent=2)
    # print(json_string)
    
    return json_string
        
def embedding(recipes) -> list:
    #texts
    name_texts = [recipe["Recipe name"] for recipe in recipes]
    ingredients_texts = [recipe["Ingredients"] for recipe in recipes]
    instructions_texts = [recipe["Instructions"] for recipe in recipes]
    cookingtime_texts = [recipe["Cooking time"] for recipe in recipes]
    
    data = []
    #embeddings data
    name_embeddings = model.encode(name_texts, convert_to_tensor=True) 
    # print(f"Name embedding: {name_embeddings}")
    ingredients_embeddings = model.encode(ingredients_texts, convert_to_tensor=True)
    instructions_embeddings = model.encode(instructions_texts, convert_to_tensor=True)
    cookingtime_embeddings = model.encode(cookingtime_texts, convert_to_tensor=True)
    
    
    
    data.append({
        "Name Field": name_embeddings,
        "Ingredients Field": ingredients_embeddings,
        "Instructions Field": instructions_embeddings,
        "Cooking_time Field": cookingtime_embeddings
    })
    return data

def embedding_query(query: str) -> list:
    #embedding query
    query_embeddings = model.encode(query, convert_to_tensor=True)
    
    return query_embeddings
  
def similarity_scores(data: list, query: torch.Tensor, recipes: list, top_k=3) -> list:
    data_dict = data[0]
    num_recipes = len(recipes)
    all_scores = np.zeros((num_recipes, len(data_dict)))
    print(all_scores.shape)
    
    fields = list(data_dict.keys())
    for field_idx, (field, embeddings) in enumerate(data_dict.items()):
        sim = util.cos_sim(query, embeddings).cpu().numpy().flatten()
        all_scores[:, field_idx] = sim
    
    avg_scores = np.mean(all_scores, axis=1)
    
    sorted_indices = np.argsort(avg_scores)[::-1][:top_k]
    
    top_recipes = []
    for idx in sorted_indices:
        recipe = recipes[idx].copy()
        recipe["average_similarity"] = avg_scores[idx]
        top_recipes.append(recipe)
    
    print(f"Top Recipes: {top_recipes}")
    return top_recipes
        
    
if __name__ == "__main__":
    recipes = sample(db_path=db_path)
    query = "Which recipes is made from mushroom?"
    
    recipes = json.loads(recipes)
    
    data_embeddings = embedding(recipes=recipes)
    query_embeddings = embedding_query(query=query)
    
    # Print shapes of embeddings in data_embeddings
    for data_dict in data_embeddings:
        for field, embedding in data_dict.items():
            print(f"Shape of {field}: {embedding.shape}")
    
    print(f"Shape of query_embeddings: {query_embeddings.shape}")
    
    # Compute and print top 3 recipes
    top_recipes = similarity_scores(data_embeddings, query_embeddings, recipes, top_k=3)
    print("Top 3 recipes có similarity cao nhất:")
    for recipe in top_recipes:
        print(json.dumps(recipe, indent=2))
    