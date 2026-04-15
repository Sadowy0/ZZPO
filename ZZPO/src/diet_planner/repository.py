from __future__ import annotations

import json
from pathlib import Path

from .models import Meal, Nutrition


class MealRepository:
    def __init__(self, data_path: Path) -> None:
        self._data_path = data_path
        self._cache: list[Meal] | None = None

    def all(self) -> list[Meal]:
        if self._cache is None:
            self._cache = self._load()
        return list(self._cache)

    def filter_by_preferences(self, preferences: set[str]) -> list[Meal]:
        meals = self.all()
        if not preferences:
            return meals
        return [meal for meal in meals if preferences.issubset(meal.tags)]

    def _load(self) -> list[Meal]:
        payload = json.loads(self._data_path.read_text(encoding="utf-8"))
        meals: list[Meal] = []

        for item in payload:
            nutrition_payload = item["nutrition"]
            meals.append(
                Meal(
                    id=item["id"],
                    name=item["name"],
                    meal_type=item["meal_type"],
                    nutrition=Nutrition(
                        calories=int(nutrition_payload["calories"]),
                        protein_g=float(nutrition_payload["protein_g"]),
                        fat_g=float(nutrition_payload["fat_g"]),
                        carbs_g=float(nutrition_payload["carbs_g"]),
                    ),
                    prep_minutes=int(item["prep_minutes"]),
                    tags=set(item.get("tags", [])),
                    ingredients=tuple(item.get("ingredients", [])),
                )
            )

        return meals
