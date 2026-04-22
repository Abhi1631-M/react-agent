Here's your README. Create `README.md` in your `react-agent` folder and paste this:

```markdown
# ReAct Agent 🤖

An AI agent that thinks step by step and decides which tool to use 
on its own — web search, calculator, or Python runner.

## How It Works

```
User question
     ↓
Agent thinks → picks a tool → uses it → observes result
     ↓
Repeats until it has the final answer
     ↓
Final answer
```

## Tools Available

| Tool | What it does |
|---|---|
| web_search | Searches the internet for real-time information |
| calculator | Evaluates math expressions precisely |
| python_runner | Writes and runs Python code on the fly |

## Example Queries

```
what is 15 percent of 85000
→ Uses calculator → 12750.0

who is the prime minister of India
→ Uses web search → Narendra Modi

write python code to print fibonacci series up to 10 numbers and run it
→ Uses python runner → [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

search for the price of gold per gram and calculate cost of 10 grams
→ Uses web search + calculator (multi-step reasoning)
```

## Setup

1. Clone the repo
   ```bash
   git clone https://github.com/Abhi1631-M/react-agent.git
   cd react-agent
   ```

2. Create virtual environment
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   python -m pip install -r requirements.txt
   ```

4. Create `.env` file
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

5. Run
   ```bash
   python agent.py
   ```

## What is ReAct?

ReAct = **Reason + **Act**. The agent follows this loop:

```
Thought  → what do I need to do?
Action   → which tool should I use?
Input    → what do I send to the tool?
Observation → what did the tool return?
... repeat until ...
Final Answer → done
```

This is the foundation of every AI assistant, Copilot, and 
autonomous agent system built today.

## Tech Stack
- Python 3.12
- LangChain
- Groq API — Llama 3.3 70B
- DuckDuckGo Search — free real-time web search
- numexpr — safe math evaluation
```


```

Done! 🚀
