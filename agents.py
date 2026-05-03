from crewai import Agent, LLM
from tools import list_directory, read_file
import os

# Helper to select LLM based on environment variables
def get_llm():
    # Use environment variable for model name, default to qwen2.5:3b (new, faster model)
    ollama_model = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")
    
    # Prioritize local Ollama if no API keys are found or if explicitly requested
    if os.getenv("USE_OLLAMA") == "true" or (not os.getenv("OPENAI_API_KEY") and not os.getenv("GOOGLE_API_KEY") and not os.getenv("GROQ_API_KEY")):
        print(f"Using local open-source LLM (Ollama - {ollama_model})...")
        return LLM(model=f"ollama/{ollama_model}", temperature=0.2, base_url="http://localhost:11434")
    elif os.getenv("GROQ_API_KEY"):
        print("Using Groq API (llama-3.3-70b-versatile)...")
        return LLM(model="groq/llama-3.3-70b-versatile", temperature=0.2)
    elif os.getenv("OPENAI_API_KEY"):
        return LLM(model="gpt-4o", temperature=0.2)
    elif os.getenv("GOOGLE_API_KEY"):
        return LLM(model="gemini/gemini-1.5-pro-latest", temperature=0.2)
    else:
        print(f"Falling back to local open-source LLM (Ollama - {ollama_model})...")
        return LLM(model=f"ollama/{ollama_model}", temperature=0.2, base_url="http://localhost:11434")

def create_architect_agent():
    return Agent(
        role='Project Architect',
        goal='Understand the developer prompt, analyze the repository structure, and guide the analysis.',
        backstory="You are an expert software architect. You can quickly understand a project's purpose from a short prompt and figure out how the codebase is structured.",
        verbose=True,
        allow_delegation=False,  # Disabled to prevent hidden OpenAI function-calling calls
        tools=[list_directory, read_file],
        llm=get_llm(),
        respect_context_window=False  # Prevents OpenAI summarization calls
    )

def create_analyzer_agent():
    return Agent(
        role='Code Analyzer',
        goal='Deep dive into specific files and modules to find logic errors, syntax issues, or bugs based on the intended project behavior.',
        backstory='You are a meticulous senior software engineer. You notice every tiny detail and bug that others miss. You collaborate to figure out if the project works as the developer intends.',
        verbose=True,
        allow_delegation=False,
        tools=[list_directory, read_file],
        llm=get_llm(),
        respect_context_window=False  # Prevents OpenAI summarization calls
    )

def create_liaison_agent():
    return Agent(
        role='Copilot Liaison Reporter',
        goal='Compile all findings and errors into a clean, highly structured Markdown report designed to be fed into GitHub Copilot or ChatGPT to generate fixes.',
        backstory='You are a technical writer and developer advocate. You know exactly what context AI Copilots need to fix bugs effectively. You produce structured, actionable reports.',
        verbose=True,
        allow_delegation=False,
        llm=get_llm(),
        respect_context_window=False  # Prevents OpenAI summarization calls
    )
