# Blueprint AI Fellowship - Week 4: Tool Use and Function Calling

## Project Overview

A Python tutorial script demonstrating LLM tool use and function calling using the Groq API (via OpenAI-compatible client). This is a console-based educational project with no frontend.

## Project Structure

```
week4-starter/
  main.py                  - Main tutorial script with 5 parts demonstrating tool use
  tools.py                 - Tool functions (calculate, get_weather, check_availability,
                             first_free_slot, parse_transcript, calculate_gpa,
                             reapply_repeat_policy, lookup_professor, lookup_requirements)
  schedule.py              - Sample weekly schedule data for calendar tools
  scrape_rmp.py            - One-time scraper for Rutgers professors on Rate My Professor
  scrape_requirements.py   - One-time scraper for Rutgers major/minor degree requirements
  requirements.txt         - Python dependencies (openai, requests)
  lib/
    transcript.txt               - Raw university transcript for GPA calculation
    Data/
      parsed_transcript.json     - Pre-parsed transcript (avoids re-parsing each run)
      rutgers_professors.json    - Scraped RMP data (7,192 professors)
      SAS/
        computer-science-BS.json - CS B.S. requirements (core, electives, physics/chem, residency)
        data-science-BS.json     - Data Science B.S. requirements (all sections)
        SAS-CORE/
          R1_Contemporary_Challenges.json
          R2_Natural_Sciences.json
          R3_Social_Historical.json
          R4_Arts_Humanities.json
          R5_Writing_Communication.json
          R6_Quantitative_Reasoning.json
```

## Setup

- **Language**: Python 3.12
- **Packages**: openai, requests, beautifulsoup4
- **API**: Groq API (OpenAI-compatible) at https://api.groq.com/openai/v1
- **Model**: llama-3.3-70b-versatile
- **Required Secret**: GROQ_API_KEY

## Running

The workflow runs `cd week4-starter && python main.py` as a console workflow.
Parts 1-4 are commented out to save Groq tokens. Only Part 5 (double major planning) runs.

## Scripts

- **main.py**: Run via workflow. Part 5 active: double major CS+DS path planning.
- **scrape_rmp.py**: One-time. Scrapes all Rutgers-NB professors from RMP (GraphQL API).
  - Outputs to `lib/Data/rutgers_professors.json`
- **scrape_requirements.py**: One-time. Fetches CS, DS, Math, Stats degree pages.
  - Outputs to `lib/Data/SAS/` (does not overwrite user-curated JSONs there)

## Tools Available

| Tool | Description |
|------|-------------|
| `calculate` | Evaluate math expressions |
| `get_weather` | Get weather via wttr.in API |
| `check_availability` | Check schedule for a day/time |
| `first_free_slot` | Find earliest free slot of given duration |
| `parse_transcript` | Parse raw transcript text into structured JSON |
| `calculate_gpa` | Calculate GPA from parsed transcript |
| `reapply_repeat_policy` | Re-apply repeat/exclusion policy to transcript |
| `lookup_professor` | Search Rutgers professors by name (from RMP data) |
| `lookup_requirements` | Look up major/minor requirements by department + degree type |

## lookup_requirements Tool

- **Departments**: `Computer Science` (or `cs`), `Data Science` (or `ds`), `Mathematics` (or `math`), `Statistics` (or `stats`), `SAS Core` (or `core`)
- **Degree types**: `BS`, `BA`, `minor`, `major`, `all`
- Auto-indexes files by their embedded `major_name` + `degree_type` fields
- Requesting `SAS Core` returns all R1–R6 SAS core requirement sections

## Notes

- Retry logic (3 attempts) on all API calls for Groq `tool_use_failed` errors
- Transcript parser handles `E`-flag (excluded repeats) for accurate GPA
- Spring 2026 courses are in-progress (no grades), excluded from GPA
- `_REQUIREMENTS_DIR` = `lib/Data/SAS/` — add new `.json` files there to auto-register them
