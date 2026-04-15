from __future__ import annotations

import json
from collections import Counter
from datetime import date, timedelta
from pathlib import Path
from random import Random

from .models import ActivityLevel, DailyPlan, Gender, Goal, Meal, Nutrition, UserProfile, WeeklyPlan
from .repository import MealRepository


class NutritionService:
    def estimate_daily_calories(self, profile: UserProfile) -> int:
        if profile.gender is Gender.MALE:
            bmr = 10 * profile.weight_kg + 6.25 * profile.height_cm - 5 * profile.age + 5
        else:
            bmr = 10 * profile.weight_kg + 6.25 * profile.height_cm - 5 * profile.age - 161

        tdee = bmr * float(profile.activity_level)
        goal_adjustment = {
            Goal.LOSE: -300,
            Goal.MAINTAIN: 0,
            Goal.GAIN: 250,
        }
        return max(1200, int(round(tdee + goal_adjustment[profile.goal])))

    def estimate_macro_target(self, profile: UserProfile, calories: int) -> Nutrition:
        protein_factor = {
            Goal.LOSE: 1.8,
            Goal.MAINTAIN: 1.6,
            Goal.GAIN: 1.9,
        }[profile.goal]

        protein_g = round(profile.weight_kg * protein_factor, 1)
        fat_g = round(profile.weight_kg * 0.9, 1)

        calories_from_protein = protein_g * 4
        calories_from_fat = fat_g * 9
        remaining_calories = max(0.0, calories - calories_from_protein - calories_from_fat)
        carbs_g = round(remaining_calories / 4, 1)

        return Nutrition(
            calories=calories,
            protein_g=protein_g,
            fat_g=fat_g,
            carbs_g=carbs_g,
        )


class MealPlannerService:
    def __init__(self, meal_repository: MealRepository, rng_seed: int = 42) -> None:
        self._meal_repository = meal_repository
        self._nutrition_service = NutritionService()
        self._rng = Random(rng_seed)

    def create_weekly_plan(self, profile: UserProfile, start_day: date | None = None) -> WeeklyPlan:
        meals = self._meal_repository.filter_by_preferences(profile.dietary_preferences)
        if len(meals) < profile.daily_meals:
            raise ValueError(
                "Not enough meals for selected preferences. Try fewer preferences or add more meal data."
            )

        target_calories = self._nutrition_service.estimate_daily_calories(profile)
        macro_target = self._nutrition_service.estimate_macro_target(profile, target_calories)

        first_day = start_day or date.today()
        days: list[DailyPlan] = []

        rotating_pool = meals.copy()
        for offset in range(7):
            self._rng.shuffle(rotating_pool)
            day_meals = self._plan_day(rotating_pool, profile.daily_meals, target_calories)
            days.append(
                DailyPlan(
                    day=first_day + timedelta(days=offset),
                    meals=day_meals,
                    target_calories=target_calories,
                )
            )

        return WeeklyPlan(days=days, macro_target=macro_target)

    def _plan_day(self, meals: list[Meal], daily_meals: int, target_calories: int) -> list[Meal]:
        remaining_calories = target_calories
        available = meals.copy()
        selected: list[Meal] = []

        for slot_index in range(daily_meals):
            slots_left = max(1, daily_meals - slot_index)
            ideal_per_meal = remaining_calories / slots_left
            chosen = min(available, key=lambda meal: abs(meal.nutrition.calories - ideal_per_meal))

            selected.append(chosen)
            remaining_calories -= chosen.nutrition.calories

            if len(available) > 1:
                available.remove(chosen)

        return selected


class ShoppingListService:
    def build_for_week(self, plan: WeeklyPlan) -> dict[str, int]:
        counts: Counter[str] = Counter()
        for meal in plan.iter_meals():
            for ingredient in meal.ingredients:
                counts[ingredient] += 1

        return dict(sorted(counts.items(), key=lambda item: item[0]))


class PlanExporter:
    @staticmethod
    def save(plan: WeeklyPlan, output_path: Path) -> None:
        payload = {
            "macro_target": {
                "calories": plan.macro_target.calories,
                "protein_g": plan.macro_target.protein_g,
                "fat_g": plan.macro_target.fat_g,
                "carbs_g": plan.macro_target.carbs_g,
            },
            "days": [
                {
                    "day": day.day.isoformat(),
                    "target_calories": day.target_calories,
                    "total": {
                        "calories": day.total_nutrition.calories,
                        "protein_g": day.total_nutrition.protein_g,
                        "fat_g": day.total_nutrition.fat_g,
                        "carbs_g": day.total_nutrition.carbs_g,
                    },
                    "meals": [
                        {
                            "id": meal.id,
                            "name": meal.name,
                            "meal_type": meal.meal_type,
                            "calories": meal.nutrition.calories,
                            "protein_g": meal.nutrition.protein_g,
                            "fat_g": meal.nutrition.fat_g,
                            "carbs_g": meal.nutrition.carbs_g,
                        }
                        for meal in day.meals
                    ],
                }
                for day in plan.days
            ],
        }

        output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
