import warnings
warnings.filterwarnings("ignore")
import os
import numexpr as ne
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.tools import Tool
from langchain_core.prompts import PromptTemplate
from duckduckgo_search import DDGS

load_dotenv(override=True)

# ── 1. LLM ────────────────────────────────────────────────
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.environ.get("GROQ_API_KEY"),
    temperature=0
)

# ── 2. Tools ──────────────────────────────────────────────

# Tool 1 — Web Search
def search_web(query):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
            if not results:
                return "No results found."
            return "\n".join([r["title"] + ": " + r["body"] for r in results])
    except Exception as e:
        return f"Search error: {e}"

search_tool = Tool(
    name="web_search",
    func=search_web,
    description="""Useful for searching current information on the internet.
    Use this when you need facts, news, or real-time data.
    Input should be a search query string."""
)

# Tool 2 — Calculator
def calculate(expression):
    try:
        result = ne.evaluate(expression)
        return str(result)
    except Exception as e:
        return f"Error: {e}"

calculator_tool = Tool(
    name="calculator",
    func=calculate,
    description="""Useful for math calculations.
    Input should be a valid math expression like '100 * 0.2' or '(50 + 30) / 4'.
    Always use this for any arithmetic."""
)

# Tool 3 — Python Runner
def run_python(code):
    try:
        import io
        import contextlib
        # Strip markdown code fences if agent wraps code in them
        code = code.strip()
        if code.startswith("```"):
            lines = code.split("\n")
            lines = [l for l in lines if not l.strip().startswith("```")]
            code = "\n".join(lines)
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exec(code, {})
        return output.getvalue() or "Code ran successfully with no output."
    except Exception as e:
        return f"Error: {e}"

python_tool = Tool(
    name="python_runner",
    func=run_python,
    description="""Useful for running Python code.
    Use this for data processing, complex logic, or generating output.
    Input should be valid Python code as a string."""
)

tools = [search_tool, calculator_tool, python_tool]

# ── 3. ReAct Prompt ───────────────────────────────────────
react_prompt = PromptTemplate.from_template("""
You are a helpful AI assistant with access to tools.
Answer the question as best you can using the tools available.

You have access to the following tools:
{tools}

Use this format STRICTLY:

Question: the input question you must answer
Thought: think about what to do
Action: the action to take, must be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (repeat Thought/Action/Action Input/Observation as needed)
Thought: I now know the final answer
Final Answer: the final answer to the original question

Begin!

Question: {input}
Thought: {agent_scratchpad}
""")

# ── 4. Create Agent ───────────────────────────────────────
agent = create_react_agent(llm=llm, tools=tools, prompt=react_prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=5,
    handle_parsing_errors=True
)

# ── 5. Chat Loop ──────────────────────────────────────────
def main():
    print("\nReAct Agent Ready!")
    print("Tools: web search, calculator, python runner")
    print("-" * 50)

    while True:
        question = input("\nYou: ").strip()

        if question.lower() == "quit":
            print("Goodbye!")
            break

        if not question:
            continue

        try:
            print("\n--- Agent Thinking ---")
            result = agent_executor.invoke({"input": question})
            print("\n--- Final Answer ---")
            print(result["output"])
            print("-" * 50)

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()