"""
Sample weekly schedule for the calendar tools.
Each day maps to a list of events with start and end times (24-hour format).
Feel free to edit this to match your own schedule!
"""

SCHEDULE = {
    "Monday": [
        {"start": "09:00", "end": "10:15", "event": "Intro to Data Science"},
        {"start": "11:30", "end": "12:50", "event": "Linear Algebra"},
        {"start": "14:00", "end": "15:00", "event": "Lunch with study group"},
        {"start": "18:00", "end": "19:30", "event": "Blueprint board meeting"},
    ],
    "Tuesday": [
        {"start": "10:00", "end": "11:20", "event": "Intro to AI"},
        {"start": "13:00", "end": "14:20", "event": "Technical Writing"},
        {"start": "16:00", "end": "17:00", "event": "Office hours with Prof. Chen"},
        {"start": "21:00", "end": "22:30", "event": "Blueprint AI Fellowship"},
    ],
    "Wednesday": [
        {"start": "09:00", "end": "10:15", "event": "Intro to Data Science"},
        {"start": "11:30", "end": "12:50", "event": "Linear Algebra"},
        {"start": "15:00", "end": "16:30", "event": "Career fair prep workshop"},
    ],
    "Thursday": [
        {"start": "10:00", "end": "11:20", "event": "Intro to AI"},
        {"start": "13:00", "end": "14:20", "event": "Technical Writing"},
        {"start": "19:00", "end": "20:00", "event": "Gym"},
    ],
    "Friday": [
        {"start": "09:00", "end": "10:00", "event": "Research meeting"},
        {"start": "12:00", "end": "13:00", "event": "Lunch"},
    ],
    "Saturday": [],
    "Sunday": [
        {"start": "14:00", "end": "16:00", "event": "Study session at Alexander Library"},
    ],
}
