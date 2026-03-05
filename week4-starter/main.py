"""
Blueprint AI Fellowship - Week 4: Tool Use and Function Calling
================================================================
This file has five parts. We work through them together during
the session, uncommenting one section at a time.

Make sure you have:
  1. GROQ_API_KEY in your Replit Secrets tab
  2. Installed packages: pip install openai requests
"""

import os
import json
from openai import OpenAI

client = OpenAI(base_url="https://api.groq.com/openai/v1",
                api_key=os.environ["GROQ_API_KEY"])

MODEL = "llama-3.3-70b-versatile"

# ============================================================
# PART 1: Your First Tool Call
# ============================================================
# This defines a calculator tool and sends a math question.
# Instead of answering directly, the model asks to use the tool.
#
# What to observe: The response has no text answer. Instead,
# check tool_calls to see the model chose "calculate" and
# generated the arguments.
# ============================================================

# print("=" * 60)
# print("PART 1: Your First Tool Call")
# print("=" * 60)

# Define a tool the LLM can use
calculator_tool = {
    "type": "function",
    "function": {
        "name": "calculate",
        "description":
        "Perform basic math. Use this for any arithmetic question.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type":
                    "string",
                    "description":
                    "A math expression to evaluate, e.g. '145 * 3.7'"
                }
            },
            "required": ["expression"]
        }
    }
}

# response = client.chat.completions.create(model=MODEL,
#                                           messages=[{
#                                               "role":
#                                               "user",
#                                               "content":
#                                               "What is 1,847 divided by 23?"
#                                           }],
#                                           tools=[calculator_tool])
#
# message = response.choices[0].message
#
# # The model does NOT answer with text. It requests a tool call.
# print(f"Text content: {message.content}")
# print(f"Tool calls: {message.tool_calls}")
#
# if message.tool_calls:
#     tc = message.tool_calls[0]
#     print(f"\nThe model wants to call: {tc.function.name}")
#     print(f"With arguments: {tc.function.arguments}")
#     print(f"Tool call ID: {tc.id}")
# print()

# ============================================================
# PART 2: The Tool Use Loop
# ============================================================
# This completes the full cycle:
#   1. Send message with tools
#   2. Model returns tool_calls
#   3. YOUR code runs the function
#   4. Send tool result back
#   5. Model writes final answer
#
# What to observe: The model never runs code. It proposes a
# call, you execute it, and feed the result back.
# ============================================================

# Uncomment the section below when ready:

from tools import calculate, calculate_gpa

# print("=" * 60)
# print("PART 2: The Tool Use Loop")
# print("=" * 60)
#
# response = client.chat.completions.create(
#     model=MODEL,
#     messages=[{
#         "role": "user",
#         "content": "What is 15% tip on a $47.50 bill?"
#     }],
#     tools=[calculator_tool])
#
# message = response.choices[0].message
# print(f"Model wants to call: {message.tool_calls[0].function.name}")
# print(f"Arguments: {message.tool_calls[0].function.arguments}")
#
# tool_call = message.tool_calls[0]
# args = json.loads(tool_call.function.arguments)
# result = calculate(args["expression"])
# print(f"Function returned: {result}")
#
# followup = client.chat.completions.create(
#     model=MODEL,
#     messages=[
#         {
#             "role": "user",
#             "content": "What is 15% tip on a $47.50 bill?"
#         },
#         message,
#         {
#             "role": "tool",
#             "tool_call_id": tool_call.id,
#             "content": result
#         }
#     ],
#     tools=[calculator_tool])
#
# print(f"\nFinal answer: {followup.choices[0].message.content}")
# print()

# ============================================================
# PART 3: Multiple Tools
# ============================================================
# This adds a weather tool alongside the calculator. The model
# picks the right tool based on the question.
#
# What to observe: Ask a weather question, a math question, and
# a general knowledge question. Watch the model pick the right
# tool (or skip tools entirely for general knowledge).
# ============================================================

# Uncomment the section below when ready:

from tools import TOOL_FUNCTIONS

# print("=" * 60)
# print("PART 3: Multiple Tools")
# print("=" * 60)

# Define both tools
weather_tool = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description":
        "Get the current weather for a city. Use this when someone asks about weather or temperature.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type":
                    "string",
                    "description":
                    "The city name, e.g. 'New Brunswick' or 'New York'"
                }
            },
            "required": ["city"]
        }
    }
}

all_tools = [calculator_tool, weather_tool]


# Helper function: run the full tool use loop
def ask_with_tools(question, tools, max_retries=3):
    print(f"\nQ: {question}")

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(model=MODEL,
                                                      messages=[{
                                                          "role":
                                                          "user",
                                                          "content":
                                                          question
                                                      }],
                                                      tools=tools)
            message = response.choices[0].message
            break
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"   (Retrying due to API error: {e})")
                continue
            print(f"   Error: {e}")
            return

    # If no tool call, the model answered directly
    if not message.tool_calls:
        print(f"A (no tool): {message.content}")
        return

    # Process tool call
    tool_call = message.tool_calls[0]
    func_name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    print(f"   Tool: {func_name}({args})")

    # Execute the function
    func = TOOL_FUNCTIONS[func_name]
    result = func(**args)
    print(f"   Result: {result}")

    # Send result back for final answer
    try:
        followup = client.chat.completions.create(model=MODEL,
                                                  messages=[{
                                                      "role": "user",
                                                      "content": question
                                                  }, message, {
                                                      "role":
                                                      "tool",
                                                      "tool_call_id":
                                                      tool_call.id,
                                                      "content":
                                                      result
                                                  }],
                                                  tools=tools)
        print(f"A: {followup.choices[0].message.content}")
    except Exception as e:
        print(f"   Result from tool: {result}")
        print(f"   (Could not get final answer from model: {e})")


# Test with different types of questions
# ask_with_tools("What is the weather in New Brunswick, NJ?", all_tools)
# ask_with_tools("What is 234 times 56?", all_tools)
# ask_with_tools("What is the capital of France?", all_tools)
# print()

# ============================================================
# PART 4: Calendar Tool with Structured Data
# ============================================================
# This adds schedule-checking tools that use the hardcoded
# weekly schedule in schedule.py. The LLM has no idea what
# your schedule looks like until it calls the tool.
#
# What to observe: The model translates natural language
# ("Thursday afternoon") into structured arguments that
# your function can process.
# ============================================================

# Uncomment the section below when ready:

from tools import TOOL_FUNCTIONS

# print("=" * 60)
# print("PART 4: Calendar Tools")
# print("=" * 60)

# Define calendar tools
availability_tool = {
    "type": "function",
    "function": {
        "name": "check_availability",
        "description":
        "Check if a specific time on a given day is free or busy. Use this when someone asks if they have something scheduled at a particular time.",
        "parameters": {
            "type": "object",
            "properties": {
                "day": {
                    "type": "string",
                    "description": "Day of the week, e.g. 'Monday', 'Tuesday'"
                },
                "time": {
                    "type": "string",
                    "description":
                    "Time in 24-hour format, e.g. '14:00' for 2pm"
                }
            },
            "required": ["day", "time"]
        }
    }
}

free_slot_tool = {
    "type": "function",
    "function": {
        "name": "first_free_slot",
        "description":
        "Find the earliest free time slot of a given duration on a specific day. Use this when someone wants to find open time in their schedule.",
        "parameters": {
            "type": "object",
            "properties": {
                "day": {
                    "type": "string",
                    "description": "Day of the week, e.g. 'Monday', 'Tuesday'"
                },
                "duration_minutes": {
                    "type": "integer",
                    "description": "How many minutes the slot needs to be"
                }
            },
            "required": ["day", "duration_minutes"]
        }
    }
}

calendar_tools = [availability_tool, free_slot_tool]

# Reuse the helper from Part 3 (already defined above with retry logic)

# ask_with_tools("Am I free at 3pm on Wednesday?", calendar_tools)
# ask_with_tools("Find me a 60-minute free slot on Tuesday", calendar_tools)
# ask_with_tools("Am I free at 10am on Thursday?", calendar_tools)
# ask_with_tools(
#     "When is my first opening on Monday that is at least 90 minutes?",
#     calendar_tools)
# print()

# ============================================================
# PART 5: Multi-Tool Chaining
# ============================================================
# This gives the model ALL tools at once and asks questions
# that require more than one tool call to answer.
#
# What to observe: The model may return multiple tool_calls
# in one response, or call one tool and then request another.
# This chaining is the bridge to next week's topic: agents.
# ============================================================

# Uncomment the section below when ready:

from tools import TOOL_FUNCTIONS

# print("=" * 60)
# print("PART 5: Multi-Tool Chaining")
# print("=" * 60)

parse_transcript_tool = {
    "type": "function",
    "function": {
        "name": "parse_transcript",
        "description":
        "Parse a raw university transcript text into structured data with terms and courses. Use this when given raw transcript text that needs to be parsed.",
        "parameters": {
            "type": "object",
            "properties": {
                "raw_text": {
                    "type": "string",
                    "description": "The raw transcript text to parse"
                }
            },
            "required": ["raw_text"]
        }
    }
}

calculate_gpa_tool = {
    "type": "function",
    "function": {
        "name": "calculate_gpa",
        "description":
        "Calculate the GPA from a parsed transcript JSON string. Use this after parsing a transcript to compute the student's GPA.",
        "parameters": {
            "type": "object",
            "properties": {
                "transcript_json": {
                    "type":
                    "string",
                    "description":
                    "A JSON string of the parsed transcript (output from parse_transcript)"
                }
            },
            "required": ["transcript_json"]
        }
    }
}

reapply_repeat_policy_tool = {
    "type": "function",
    "function": {
        "name": "reapply_repeat_policy",
        "description":
        "Reapply the university repeat/exclusion policy to a parsed transcript. Courses with a repeat flag will be excluded from GPA calculation.",
        "parameters": {
            "type": "object",
            "properties": {
                "transcript_json": {
                    "type":
                    "string",
                    "description":
                    "A JSON string of the parsed transcript to apply the repeat policy to"
                }
            },
            "required": ["transcript_json"]
        }
    }
}

lookup_professor_tool = {
    "type": "function",
    "function": {
        "name": "lookup_professor",
        "description":
        "Look up a Rutgers University professor on Rate My Professor by name. Returns their rating, difficulty, department, number of reviews, and would-take-again percentage.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type":
                    "string",
                    "description":
                    "The professor's name to search for, e.g. 'Sesh Venugopal' or 'Venugopal'"
                }
            },
            "required": ["name"]
        }
    }
}

all_tools = [
    calculator_tool, weather_tool, availability_tool, free_slot_tool,
    calculate_gpa_tool, parse_transcript_tool, reapply_repeat_policy_tool,
    lookup_professor_tool
]


def ask_multi_tool(question, tools, max_retries=3):
    """Handle questions that may require multiple tool calls."""
    # print(f"\nQ: {question}")
    messages = [{"role": "user", "content": question}]

    max_rounds = 5
    for round_num in range(max_rounds):
        for attempt in range(max_retries):
            try:
                response = client.chat.completions.create(model=MODEL,
                                                          messages=messages,
                                                          tools=tools)
                message = response.choices[0].message
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"   (Retrying due to API error: {e})")
                    continue
                print(f"   Error: {e}")
                return

        if not message.tool_calls:
            print(f"\nA: {message.content}")
            return

        messages.append(message)
        for tool_call in message.tool_calls:
            func_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            print(f"   [{round_num + 1}] {func_name}({args})")

            func = TOOL_FUNCTIONS[func_name]
            result = func(**args)
            print(f"       returned: {result}")

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

    print("(Reached max rounds without a final answer)")


# Questions that need multiple tools
# ask_multi_tool(
#     "Find me a free 60-minute slot on Wednesday and tell me what the weather will be like in New Brunswick",
#     all_tools)
# ask_multi_tool(
#     "Am I free at 2pm on Friday? Also, what is 20% tip on a $85 dinner?",
#     all_tools)

# =============================================
# GPA Calculation from transcript file
# =============================================
# import os

# transcript_path = os.path.join(os.path.dirname(__file__), "lib",
#                                "transcript.txt")
# with open(transcript_path, "r") as f:
#     transcript_text = f.read()

# ask_multi_tool(
#     f"Parse this transcript and calculate my GPA:\n\n{transcript_text}",
#     all_tools)
# print()

# =============================================
# Professor Lookup Test
# =============================================
# print("=" * 60)
# print("Professor Lookup Test")
# print("=" * 60)
# ask_multi_tool("What are the ratings for Professor Sesh Venugopal at Rutgers?",
#                all_tools)
# ask_multi_tool(
#     "Who is a better professor for Computer Science at Rutgers - Fatemeh Hafizi or Arnold Lau?",
#     all_tools)
# print()

# =============================================
# Double Major Path Planning
# =============================================
print("=" * 60)
print("Double Major Path Planning")
print("=" * 60)

import os
import json as _json

parsed_path = os.path.join(os.path.dirname(__file__), "lib", "parsed_transcript.json")
with open(parsed_path, "r") as f:
    parsed_transcript = _json.load(f)

completed_courses = []
in_progress_courses = []
for term in parsed_transcript["terms"]:
    for c in term["courses"]:
        entry = f"{c['subject']}:{c['course_number']} {c['title']}"
        if c["grade"]:
            completed_courses.append(f"{entry} (Grade: {c['grade']}, {term['term_name']})")
        else:
            in_progress_courses.append(f"{entry} (In Progress, {term['term_name']})")

completed_text = "\n".join(completed_courses)
in_progress_text = "\n".join(in_progress_courses)

professors_path = os.path.join(os.path.dirname(__file__), "lib", "rutgers_professors.json")
with open(professors_path, "r") as f:
    professors_data = _json.load(f)

cs_ds_professors = [
    p for p in professors_data
    if p["department"] in ("Computer Science", "Statistics", "Mathematics",
                           "Information Tech. & Informatics", "Data Science")
    and p["num_ratings"] > 0
]
cs_ds_professors.sort(key=lambda p: p["avg_rating"], reverse=True)
top_professors_text = "\n".join(
    f"{p['first_name']} {p['last_name']} | {p['department']} | "
    f"Rating: {p['avg_rating']}/5 | Difficulty: {p['avg_difficulty']}/5 | "
    f"Reviews: {p['num_ratings']} | Would Take Again: {p['would_take_again_pct']:.1f}%"
    for p in cs_ds_professors[:50]
)

ask_multi_tool(
    f"""I'm a student at Rutgers University - New Brunswick and I want to double major in
Computer Science (CS) and Data Science (DS). Based on my completed and in-progress courses
below, figure out what I still need.

Here are the EXACT Rutgers requirements:

BS IN COMPUTER SCIENCE REQUIREMENTS:
Core courses:
- Intro to CS (198:111)
- Data Structures (198:112)
- Discrete Structures I (198:205)
- Discrete Structures II (198:206)
- Computer Architecture (198:211)
- Systems Programming (198:214)
- Intro to AI (198:213) OR Design & Analysis of Algorithms (198:344)
Math requirements:
- Calculus I (640:151)
- Calculus II (640:152)
- Linear Algebra (640:250)
Electives: 7 total CS electives (198:xxx courses), of which at least 2 must be at the 300+ level.

DATA SCIENCE MAJOR REQUIREMENTS:
Core courses:
- Intro to CS (198:111)
- Data Structures (198:112)
- Intro to Data Science (198:142)
- Data Management (198:210)
- Regression Methods (960:401)
- Intro to Probability & Statistical Inference (960:381)
- Statistical Computing (960:467)
Math requirements:
- Calculus I (640:151)
- Calculus II (640:152)
- Linear Algebra (640:250)
Electives: 2 DS electives from approved list.

IMPORTANT: Courses that appear in BOTH majors overlap and satisfy both at once. Identify
ALL overlapping courses. Calculus II (640:152) is required for BOTH majors and has NOT
been completed yet.

MY COMPLETED COURSES:
{completed_text}

MY IN-PROGRESS COURSES (Spring 2026):
{in_progress_text}

Recommend the fastest semester-by-semester plan to finish both majors starting from
Fall 2026. For each remaining required course, look up the professor ratings and suggest
the highest-rated professor.

TOP RATED PROFESSORS IN RELEVANT DEPARTMENTS:
{top_professors_text}""",
    all_tools
)
print()
