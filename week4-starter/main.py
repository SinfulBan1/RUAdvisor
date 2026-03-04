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

print("=" * 60)
print("PART 1: Your First Tool Call")
print("=" * 60)

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

response = client.chat.completions.create(model=MODEL,
                                          messages=[{
                                              "role":
                                              "user",
                                              "content":
                                              "What is 1,847 divided by 23?"
                                          }],
                                          tools=[calculator_tool])

message = response.choices[0].message

# The model does NOT answer with text. It requests a tool call.
print(f"Text content: {message.content}")
print(f"Tool calls: {message.tool_calls}")

if message.tool_calls:
    tc = message.tool_calls[0]
    print(f"\nThe model wants to call: {tc.function.name}")
    print(f"With arguments: {tc.function.arguments}")
    print(f"Tool call ID: {tc.id}")
print()

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

print("=" * 60)
print("PART 2: The Tool Use Loop")
print("=" * 60)

# Step 1: Send message with tools
response = client.chat.completions.create(
    model=MODEL,
    messages=[{
        "role": "user",
        "content": "What is 15% tip on a $47.50 bill?"
    }],
    tools=[calculator_tool])

message = response.choices[0].message
print(f"Model wants to call: {message.tool_calls[0].function.name}")
print(f"Arguments: {message.tool_calls[0].function.arguments}")
#
# # Step 2 & 3: Extract the tool call and run the function
tool_call = message.tool_calls[0]
args = json.loads(tool_call.function.arguments)
result = calculate(args["expression"])
print(f"Function returned: {result}")

# Step 4: Send the result back to the model
followup = client.chat.completions.create(
    model=MODEL,
    messages=[
        {
            "role": "user",
            "content": "What is 15% tip on a $47.50 bill?"
        },
        message,  # the model's tool call request
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result
        }
    ],
    tools=[calculator_tool])

# Step 5: Model writes a natural language answer
print(f"\nFinal answer: {followup.choices[0].message.content}")
print()

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

print("=" * 60)
print("PART 3: Multiple Tools")
print("=" * 60)

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
ask_with_tools("What is the weather in New Brunswick, NJ?", all_tools)
ask_with_tools("What is 234 times 56?", all_tools)
ask_with_tools("What is the capital of France?", all_tools)
print()

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

print("=" * 60)
print("PART 4: Calendar Tools")
print("=" * 60)

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

ask_with_tools("Am I free at 3pm on Wednesday?", calendar_tools)
ask_with_tools("Find me a 60-minute free slot on Tuesday", calendar_tools)
ask_with_tools("Am I free at 10am on Thursday?", calendar_tools)
ask_with_tools(
    "When is my first opening on Monday that is at least 90 minutes?",
    calendar_tools)
print()

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

print("=" * 60)
print("PART 5: Multi-Tool Chaining")
print("=" * 60)

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

all_tools = [
    calculator_tool, weather_tool, availability_tool, free_slot_tool,
    calculate_gpa_tool, parse_transcript_tool, reapply_repeat_policy_tool
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
ask_multi_tool(
    "Find me a free 60-minute slot on Wednesday and tell me what the weather will be like in New Brunswick",
    all_tools)
ask_multi_tool(
    "Am I free at 2pm on Friday? Also, what is 20% tip on a $85 dinner?",
    all_tools)

# =============================================
# GPA Calculation from transcript file
# =============================================
import os

transcript_path = os.path.join(os.path.dirname(__file__), "lib",
                               "transcript.txt")
with open(transcript_path, "r") as f:
    transcript_text = f.read()

ask_multi_tool(
    f"Parse this transcript and calculate my GPA:\n\n{transcript_text}",
    all_tools)
print()
