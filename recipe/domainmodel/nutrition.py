class Nutrition:
    def __init__(self, recipe_id: int,
                 calories: float | None = None,
                 fat: float | None = None,
                 saturated_fat: float | None = None,
                 cholesterol: float | None = None,
                 sodium: float | None = None,
                 carbohydrates: float | None = None,
                 fiber: float | None = None,
                 sugar: float | None = None,
                 protein: float | None = None):
        
        if (not isinstance(recipe_id, int)) or recipe_id <= 0:
            raise ValueError("id must be a positive int.")

        if calories is not None and (not isinstance(calories, float) or calories < 0):
            raise ValueError("calories must be a non-negative float, or None.")

        if fat is not None and (not isinstance(fat, float) or fat < 0):
            raise ValueError("fat must be a non-negative float, or None.")

        if saturated_fat is not None and (not isinstance(saturated_fat, float) or saturated_fat < 0):
            raise ValueError("saturated fat must be a non-negative float, or None.")

        if cholesterol is not None and (not isinstance(cholesterol, float) or cholesterol < 0):
            raise ValueError("cholesterol must be a non-negative float, or None.")

        if sodium is not None and (not isinstance(sodium, float) or sodium < 0):
            raise ValueError("sodium must be a non-negative float, or None.")

        if carbohydrates is not None and (not isinstance(carbohydrates, float) or carbohydrates < 0):
            raise ValueError("carbohydrates must be a non-negative float, or None.")

        if fiber is not None and (not isinstance(fiber, float) or fiber < 0):
            raise ValueError("fiber must be a non-negative float, or None.")

        if sugar is not None and (not isinstance(sugar, float) or sugar < 0):
            raise ValueError("sugar must be a non-negative float, or None.")

        if protein is not None and (not isinstance(protein, float) or protein < 0):
            raise ValueError("protein must be a non-negative float, or None.")

        self.__id = recipe_id
        self.__calories = calories
        self.__fat = fat
        self.__saturated_fat = saturated_fat
        self.__cholesterol = cholesterol
        self.__sodium = sodium
        self.__carbohydrates = carbohydrates
        self.__fiber = fiber
        self.__sugar = sugar
        self.__protein = protein


    def __repr__(self) -> str:
        return f"<Nutrition {self.id}>"


    def __eq__(self, other) -> bool:
        if not isinstance(other, Nutrition):
            return False
        return self.id == other.id
    
    
    def __lt__(self, other) -> bool:
        if not isinstance(other, Nutrition):
            raise TypeError("Comparison must be between Nutrition instances")
        return self.id < other.id


    def __hash__(self) -> int:
        return hash(self.__id)


    @property
    def id(self) -> int:
        return self.__id

    @property
    def calories(self) -> float | None:
        return self.__calories
        
    @property
    def fat(self) -> float | None:
        return self.__fat

    @property
    def saturated_fat(self) -> float | None:
        return self.__saturated_fat

    @property
    def saturated_fat(self) -> float | None:
        return self.__saturated_fat

    @property
    def cholesterol(self) -> float | None:
        return self.__cholesterol
    
    @property
    def sodium(self) -> float | None:
        return self.__sodium

    @property
    def carbohydrates(self) -> float | None:
        return self.__carbohydrates

    @property
    def fiber(self) -> float | None:
        return self.__fiber

    @property
    def sugar(self) -> float | None:
        return self.__sugar

    @property
    def protein(self) -> float | None:
        return self.__protein