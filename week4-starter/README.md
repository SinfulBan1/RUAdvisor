# Week 4: Tool Use and Function Calling

Blueprint AI Fellowship | Spring 2026

## Setup

1. Add your API key in the **Secrets** tab (Tools > Secrets):
   - `GROQ_API_KEY`

2. Install packages in the **Shell** tab:
   ```
   pip install llama-index llama-index-llms-groq llama-index-embeddings-voyageai llama-index-vector-stores-pinecone openai voyageai pinecone
   ```

3. Hit the green **Run** button.

## Structure

- `main.py` - Workshop code (5 parts, uncomment as we go)
- `tools.py` - Tool functions the LLM can call (calculator, weather, calendar)
- `schedule.py` - Sample weekly schedule data for the calendar tools
- `requirements.txt` - Python dependencies

## Workshop Parts

1. **Your First Tool Call** - Define a calculator tool, see the model request it
2. **The Tool Use Loop** - Complete the full cycle: call, execute, return, answer
3. **Multiple Tools** - Add weather, watch the model pick the right tool
4. **Calendar Tools** - Check availability and find free slots with structured data
5. **Multi-Tool Chaining** - Questions that need more than one tool to answer
