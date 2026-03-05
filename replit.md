# Blueprint AI Fellowship - Week 4: Tool Use and Function Calling

## Project Overview

A Python tutorial script demonstrating LLM tool use and function calling using the Groq API (via OpenAI-compatible client). This is a console-based educational project with no frontend.

## Project Structure

```
week4-starter/
  main.py              - Main tutorial script with 5 parts demonstrating tool use
  tools.py             - Tool functions (calculate, get_weather, check_availability,
                         first_free_slot, parse_transcript, calculate_gpa,
                         reapply_repeat_policy, lookup_professor, lookup_requirements)
  schedule.py          - Sample weekly schedule data for calendar tools
  scrape_rmp.py        - One-time scraper for Rutgers professors on Rate My Professor
  scrape_requirements.py - One-time scraper for Rutgers major/minor degree requirements
  requirements.txt     - Python dependencies (openai, requests)
  lib/
    transcript.txt          - Sample university transcript for GPA calculation demo
    parsed_transcript.json  - Pre-parsed transcript data (avoids re-parsing each run)
    rutgers_professors.json - Scraped RMP data (7,192 professors)
    requirements/           - Scraped degree requirement JSON files
      cs/
        bs.json             - CS B.S. degree requirements
        ba.json             - CS B.A. degree requirements
        minor.json          - CS minor requirements
        electives.json      - CS electives list (all departments)
      ds/
        bs.json             - Data Science B.S. requirements (all tracks)
        ba.json             - Data Science B.A. requirements (all tracks)
        minor.json          - Data Science minor requirements
      math/
        major.json          - Mathematics major requirements (all options)
        minor.json          - Mathematics minor requirements
      stats/
        major.json          - Statistics major requirements
        minor.json          - Statistics minor requirements
```

## Setup

- **Language**: Python 3.12
- **Packages**: openai, requests
- **API**: Groq API (OpenAI-compatible) at https://api.groq.com/openai/v1
- **Model**: llama-3.3-70b-versatile
- **Required Secret**: GROQ_API_KEY

## Running

The workflow runs `cd week4-starter && python main.py` as a console workflow.

## Scripts

- **main.py**: Run via workflow. Demonstrates 5 parts of LLM tool calling.
- **scrape_rmp.py**: One-time standalone script. Run manually: `cd week4-starter && python scrape_rmp.py`
  - Scrapes all Rutgers-NB professors from Rate My Professor via GraphQL API
  - Outputs to `lib/rutgers_professors.json`
- **scrape_requirements.py**: One-time standalone script. Run manually: `cd week4-starter && python scrape_requirements.py`
  - Scrapes CS, DS, Math, and Stats major/minor requirements from Rutgers department websites
  - Outputs structured JSON to `lib/requirements/` subdirectories

## Tools Available

- **calculate**: Evaluate math expressions
- **get_weather**: Get weather via wttr.in API
- **check_availability**: Check schedule availability for a day/time
- **first_free_slot**: Find earliest free slot of given duration
- **parse_transcript**: Parse raw university transcript text into structured JSON
- **calculate_gpa**: Calculate GPA from parsed transcript data
- **reapply_repeat_policy**: Reapply repeat/exclusion policy to transcript data
- **lookup_professor**: Search Rutgers professors by name using scraped RMP data
- **lookup_requirements**: Look up Rutgers major/minor degree requirements by department and degree type

## Notes

- API calls include retry logic (up to 3 attempts) to handle Groq's occasional `tool_use_failed` errors
- The transcript parser handles the `E` (excluded) repeat flag, properly excluding those courses from GPA
- Spring 2026 courses are in-progress (no grades) and excluded from GPA calculation
- Parts 1-4 in main.py are commented out to save Groq API tokens during development
- The double major planning test (Part 5) uses lookup_requirements to fetch real scraped data instead of hardcoded requirements
- Requirements scraper fetches from live Rutgers websites: cs.rutgers.edu, ds.sas.rutgers.edu, math.rutgers.edu, statistics.rutgers.edu
