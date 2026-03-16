import json
import os
from habit import Habit
from datetime import datetime, timedelta

FILE_NAME = "habits.json"

def get_predefined_habits():
    """
    Returns 5 predefined habits with 4 weeks of dummy data.
    """
    habits = []
    
    # 1. Daily Habit: Drink Water (Good streak)
    h1 = Habit("Drink Water", "daily")
    base_date = datetime.now() - timedelta(days=28)
    for i in range(28): # 4 weeks of data
        h1.completed_dates.append((base_date + timedelta(days=i)).isoformat())
    habits.append(h1)

    # 2. Daily Habit: Read Book (Broken streak)
    h2 = Habit("Read Book", "daily")
    for i in range(14): # Only first 2 weeks
        h2.completed_dates.append((base_date + timedelta(days=i)).isoformat())
    habits.append(h2)

    # 3. Weekly Habit: Gym (Perfect streak)
    h3 = Habit("Go to Gym", "weekly")
    for i in range(4): # 4 weeks
        h3.completed_dates.append((base_date + timedelta(weeks=i)).isoformat())
    habits.append(h3)

    # 4. Weekly Habit: Grocery Shopping
    h4 = Habit("Grocery Shopping", "weekly")
    habits.append(h4) # Empty data

    # 5. Daily Habit: Meditation
    h5 = Habit("Meditation", "daily")
    habits.append(h5)

    return habits

def load_data():
    if not os.path.exists(FILE_NAME):
        return get_predefined_habits()
    
    try:
        with open(FILE_NAME, 'r') as f:
            data = json.load(f)
            return [Habit(**h) for h in data]
    except (json.JSONDecodeError, FileNotFoundError):
        return get_predefined_habits()

def save_data(habits):
    with open(FILE_NAME, 'w') as f:
        json.dump([h.to_dict() for h in habits], f, indent=4)