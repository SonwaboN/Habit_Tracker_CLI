from datetime import datetime

class Habit:
    def __init__(self, name: str, periodicity: str, creation_date: str = None, completed_dates: list = None):
        """
        Habit class to store habit details.
        :param name: Name of the habit.
        :param periodicity: 'daily' or 'weekly'.
        :param creation_date: ISO format date string.
        :param completed_dates: List of ISO format date strings.
        """
        self.name = name
        self.periodicity = periodicity
        # Use datetime.now().isoformat() if no date is provided
        self.creation_date = creation_date if creation_date else datetime.now().isoformat()
        self.completed_dates = completed_dates if completed_dates else []

    def check_off(self):
        """
        Marks the habit as complete for the current time.
        """
        self.completed_dates.append(datetime.now().isoformat())

    def to_dict(self):
        """
        Helper method to serialize the object for JSON storage.
        """
        return {
            "name": self.name,
            "periodicity": self.periodicity,
            "creation_date": self.creation_date,
            "completed_dates": self.completed_dates
        }