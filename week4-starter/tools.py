"""
Tool functions for Week 4.
These are the actual Python functions that run when the LLM requests a tool.
The LLM never sees this code. It only sees the tool schemas (defined in main.py).
"""

import requests
from schedule import SCHEDULE
import re
from collections import defaultdict
from typing import Dict


def calculate(expression: str) -> str:
    """Evaluate a math expression and return the result as a string."""
    try:
        # Only allow safe math operations
        allowed = set("0123456789+-*/.() ")
        if not all(c in allowed for c in expression):
            return "Error: expression contains invalid characters"
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {e}"


def get_weather(city: str) -> str:
    """Get current weather for a city using the free wttr.in API (no key needed)."""
    try:
        url = f"https://wttr.in/{city}?format=%C+%t+%h+%w"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return f"Weather in {city}: {response.text.strip()}"
        else:
            return f"Could not get weather for {city} (status {response.status_code})"
    except Exception as e:
        return f"Weather API error: {e}"


def check_availability(day: str, time: str) -> str:
    """Check if a specific time on a given day is free or busy."""
    day = day.capitalize()
    if day not in SCHEDULE:
        return f"No schedule data for {day}"

    events = SCHEDULE[day]
    for event in events:
        if event["start"] <= time < event["end"]:
            return f"Busy at {time} on {day}: {event['event']} ({event['start']} to {event['end']})"

    return f"Free at {time} on {day}"


def first_free_slot(day: str,
                    duration_minutes: int,
                    window_start: str = "08:00",
                    window_end: str = "22:00") -> str:
    """Find the earliest free slot of a given duration on a specific day."""
    day = day.capitalize()
    if day not in SCHEDULE:
        return f"No schedule data for {day}"

    events = sorted(SCHEDULE[day], key=lambda e: e["start"])

    def time_to_min(t):
        h, m = t.split(":")
        return int(h) * 60 + int(m)

    def min_to_time(m):
        return f"{m // 60:02d}:{m % 60:02d}"

    current = time_to_min(window_start)
    end_limit = time_to_min(window_end)

    for event in events:
        event_start = time_to_min(event["start"])
        event_end = time_to_min(event["end"])

        # Check if there's a gap before this event
        if event_start > current:
            gap = event_start - current
            if gap >= duration_minutes:
                return f"First free {duration_minutes}-minute slot on {day}: {min_to_time(current)} to {min_to_time(current + duration_minutes)}"

        # Move past this event
        if event_end > current:
            current = event_end

    # Check time after last event
    if end_limit - current >= duration_minutes:
        return f"First free {duration_minutes}-minute slot on {day}: {min_to_time(current)} to {min_to_time(current + duration_minutes)}"

    return f"No free {duration_minutes}-minute slot found on {day} between {window_start} and {window_end}"


# transcript parser

GRADE_POINTS = {
    "A": 4.0,
    "B+": 3.5,
    "B": 3.0,
    "C+": 2.5,
    "C": 2.0,
    "D": 1.0,
    "F": 0.0
}

NON_GPA_GRADES = {"W", "P", "NC", "T", "NG", "AU", "E"}

TERM_PATTERN = re.compile(r"(Fall|Spring|Summer|Winter)\s+\d{4}")
COURSE_PATTERN = re.compile(
    r"""
    ^\s*
    (?P<title>[A-Z0-9,&\-/\s]+?)\s+
    (?P<school>\d{2})\s+
    (?P<dept>\d{3})\s+
    (?P<course>\d{3})\s+
    (?P<section>\S+)\s+
    (?P<credits>\d+\.\d)\s*
    (?P<pr>E)?\s*
    (?P<grade>[A-F][+]?|W|P|NC|T|NG|AU)?
    """, re.VERBOSE)


def parse_transcript(raw_text: str) -> Dict:
    lines = raw_text.split("\n")

    transcript = {"terms": []}
    current_term = None

    for line in lines:

        # Detect semester header
        term_match = TERM_PATTERN.search(line)
        if term_match and "SCHOOL" in line:
            if current_term:
                transcript["terms"].append(current_term)

            current_term = {"term_name": term_match.group(), "courses": []}
            continue

        # Skip transfer section entirely
        if "TRANSFER COURSES" in line:
            current_term = None
            continue

        # Parse course rows
        if current_term:
            match = COURSE_PATTERN.search(line)
            if match:

                title = match.group("title").strip()
                dept = match.group("dept")
                course_number = match.group("course")
                credits = float(match.group("credits"))
                grade = match.group("grade")
                repeat_flag = match.group("pr")

                # If no grade (in progress), skip GPA inclusion
                counts_toward_gpa = (grade in GRADE_POINTS)

                course = {
                    "subject": dept,
                    "course_number": course_number,
                    "title": title,
                    "credits": credits,
                    "grade": grade,
                    "counts_toward_gpa": counts_toward_gpa,
                    "is_repeat_excluded": False,
                    "repeat_flag": repeat_flag == "E"
                }

                current_term["courses"].append(course)

    if current_term:
        transcript["terms"].append(current_term)

    _apply_repeat_policy(transcript)

    return transcript


def _apply_repeat_policy(transcript: Dict):
    course_attempts = defaultdict(list)

    for term in transcript["terms"]:
        for course in term["courses"]:
            key = f"{course['subject']}:{course['course_number']}"
            course_attempts[key].append(course)

    for attempts in course_attempts.values():
        if len(attempts) > 1:
            for course in attempts:
                if course["repeat_flag"]:
                    course["is_repeat_excluded"] = True

    for term in transcript["terms"]:
        for course in term["courses"]:
            if course["repeat_flag"] and not course["is_repeat_excluded"]:
                course["is_repeat_excluded"] = True


# gpa calculator


def calculate_gpa(transcript: Dict) -> float:
    total_points = 0.0
    total_credits = 0.0

    for term in transcript["terms"]:
        for course in term["courses"]:
            if (course["counts_toward_gpa"]
                    and not course["is_repeat_excluded"]
                    and course["grade"] in GRADE_POINTS):
                total_points += GRADE_POINTS[
                    course["grade"]] * course["credits"]
                total_credits += course["credits"]

    if total_credits == 0:
        return 0.0

    return round(total_points / total_credits, 3)


def parse_transcript_tool(raw_text: str) -> str:
    """Parse a raw transcript text and return structured JSON."""
    import json
    try:
        result = parse_transcript(raw_text)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error parsing transcript: {e}"


def calculate_gpa_tool(transcript_json: str) -> str:
    """Calculate GPA from a parsed transcript JSON string."""
    import json
    try:
        transcript = json.loads(transcript_json)
        gpa = calculate_gpa(transcript)
        return f"Calculated GPA: {gpa}"
    except Exception as e:
        return f"Error calculating GPA: {e}"


def reapply_repeat_policy(transcript_json: str) -> str:
    """Reapply the repeat/exclusion policy to a parsed transcript JSON string."""
    import json
    try:
        transcript = json.loads(transcript_json)
        _apply_repeat_policy(transcript)
        return json.dumps(transcript, indent=2)
    except Exception as e:
        return f"Error applying repeat policy: {e}"


# Map tool names to functions (used in main.py to dispatch calls)
TOOL_FUNCTIONS = {
    "calculate": calculate,
    "get_weather": get_weather,
    "check_availability": check_availability,
    "first_free_slot": first_free_slot,
    "parse_transcript": parse_transcript_tool,
    "calculate_gpa": calculate_gpa_tool,
    "reapply_repeat_policy": reapply_repeat_policy,
}
