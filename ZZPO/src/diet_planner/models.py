from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Iterable


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"


class ActivityLevel(float, Enum):
    SEDENTARY = 1.2
    LIGHT = 1.375
    MODERATE = 1.55
    HIGH = 1.725


class Goal(str, Enum):
    LOSE = "lose"
    MAINTAIN = "maintain"
    GAIN = "gain"


@dataclass(frozen=True)
class Nutrition:
    calories: int
    protein_g: float
    fat_g: float
    carbs_g: float

    def __add__(self, other: "Nutrition") -> "Nutrition":
        return Nutrition(
            calories=self.calories + other.calories,
            protein_g=round(self.protein_g + other.protein_g, 1),
            fat_g=round(self.fat_g + other.fat_g, 1),
            carbs_g=round(self.carbs_g + other.carbs_g, 1),
        )

    @staticmethod
    def zero() -> "Nutrition":
        return Nutrition(calories=0, protein_g=0.0, fat_g=0.0, carbs_g=0.0)


@dataclass(frozen=True)
class Meal:
    id: str
    name: str
    meal_type: str
    nutrition: Nutrition
    prep_minutes: int
    tags: set[str] = field(default_factory=set)
    ingredients: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class UserProfile:
    age: int
    height_cm: int
    weight_kg: float
    gender: Gender
    activity_level: ActivityLevel
    goal: Goal
    dietary_preferences: set[str] = field(default_factory=set)
    daily_meals: int = 4


@dataclass
class DailyPlan:
    day: date
    meals: list[Meal]
    target_calories: int

    @property
    def total_nutrition(self) -> Nutrition:
        total = Nutrition.zero()
        for meal in self.meals:
            total += meal.nutrition
        return total


@dataclass
class WeeklyPlan:
    days: list[DailyPlan]
    macro_target: Nutrition

    def iter_meals(self) -> Iterable[Meal]:
        for day in self.days:
            for meal in day.meals:
                yield meal
