from datetime import datetime, timedelta

def calculate_streak(completed_dates: list, periodicity: str) -> int:
    """
    Calculates the current streak for a list of dates.
    Longest streak calculation.
    """
    if not completed_dates:
        return 0
    
    # Sort dates to ensure chronological order
    dates = sorted([datetime.fromisoformat(date) for date in completed_dates])
    
    streak = 0
    current_date = datetime.now()
    
    # Iterate backwards to find the consecutive streak
    
    # Daily Logic:
    if periodicity == "daily":
        streak = 1
        for i in range(len(dates) - 1, 0, -1):
            diff = (dates[i] - dates[i-1]).days
            if diff == 1: # Consecutive day
                streak += 1
            elif diff == 0: # Same day check-off, ignore
                continue
            else:
                break 
                
    # Weekly Logic:
    elif periodicity == "weekly":
        streak = 1
        for i in range(len(dates) - 1, 0, -1):
            # Check if dates are in consecutive weeks (ISO calendar week)
            diff_weeks = dates[i].isocalendar()[1] - dates[i-1].isocalendar()[1]
            if diff_weeks == 1:
                streak += 1
            elif diff_weeks == 0:
                continue
            else:
                break
                
    return streak

def get_habits_by_periodicity(habits: list, period: str) -> list:
    """
    List habits by periodicity.
    """
    return [habit for habit in habits if habit.periodicity == period]

def get_longest_streak_all(habits: list) -> str:
    """
    Longest streak overall.
    Returns a string describing the best habit.
    """
    best_streak = 0
    best_habit = ""
    
    for habit in habits:
        streak = calculate_streak(habit.completed_dates, habit.periodicity)
        if streak > best_streak:
            best_streak = streak
            best_habit = habit.name
            
    return f"Best Habit: {best_habit} with {best_streak} streak!"