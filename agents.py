from crewai import Agent, LLM
from tools import list_directory, read_file
import os

# ---------------------------------------------------------------------------
# Block all hidden external calls from CrewAI / LiteLLM telemetry
# ---------------------------------------------------------------------------
os.environ.setdefault("OTEL_SDK_DISABLED", "true")
os.environ.setdefault("CREWAI_DISABLE_TELEMETRY", "true")
os.environ.setdefault("LITELLM_TELEMETRY", "False")
# Prevent LiteLLM from falling back to OpenAI when no key is set
os.environ.setdefault("LITELLM_LOCAL_MODEL_COST_MAP", "true")

OLLAMA_BASE = "http://localhost:11434"

# ---------------------------------------------------------------------------
# LLM selector — local-first, API as optional override via .env
# ---------------------------------------------------------------------------
def _build_ollama(model: str) -> LLM:
    """Build an Ollama LLM object pinned to local inference server."""
    return LLM(
        model=f"ollama/{model}",
        base_url=OLLAMA_BASE,
        temperature=0.2,
    )

def get_llm(role: str = "general") -> LLM:
    """
    LLM routing logic:
      1. If USE_OLLAMA=true  → always use local Ollama regardless of API keys.
      2. If API keys are present → use the cloud API (optional override).
      3. Default → local Ollama.

    Role-specific local model selection:
      - 'tool'   : llama3.1  (supports tool/function calling required by CrewAI)
      - 'report' : qwen2.5:3b (fast, great at structured text, no tool-calling needed)
      - 'general': llama3.1  (safe default)
    """
    force_local = os.getenv("USE_OLLAMA", "").lower() == "true"
    has_api_key = any([
        os.getenv("GROQ_API_KEY"),
        os.getenv("OPENAI_API_KEY"),
        os.getenv("GOOGLE_API_KEY"),
    ])

    if force_local or not has_api_key:
        # Local path — pick the best model for the role
        if role == "report":
            model = os.getenv("OLLAMA_FAST_MODEL", "qwen2.5:3b")
            print(f"[LOCAL] Using {model} for reporting (fast, structured output)")
        else:
            # Tool-calling agents need llama3.1 (phi3 doesn't support tools)
            model = os.getenv("OLLAMA_MODEL", "llama3.1")
            print(f"[LOCAL] Using {model} for {role} agent (tool-calling capable)")
        return _build_ollama(model)

    # --- Optional cloud API fallback (only if keys exist and USE_OLLAMA != true) ---
    if os.getenv("GROQ_API_KEY"):
        print("[API] Using Groq — llama-3.3-70b-versatile")
        return LLM(model="groq/llama-3.3-70b-versatile", temperature=0.2)
    if os.getenv("OPENAI_API_KEY"):
        print("[API] Using OpenAI — gpt-4o")
        return LLM(model="gpt-4o", temperature=0.2)
    if os.getenv("GOOGLE_API_KEY"):
        print("[API] Using Google — gemini-1.5-pro")
        return LLM(model="gemini/gemini-1.5-pro-latest", temperature=0.2)

    # Should not reach here, but safety net
    print("[LOCAL] Fallback to llama3.1")
    return _build_ollama("llama3.1")


# ---------------------------------------------------------------------------
# Agent factory functions
# ---------------------------------------------------------------------------

def create_architect_agent():
    """Architect reads the repo tree and key files — needs tool-calling support."""
    return Agent(
        role='Project Architect',
        goal='Understand the developer prompt, analyze the repository structure, and guide the analysis.',
        backstory=(
            "You are an expert software architect. You can quickly understand a project's "
            "purpose from a short prompt and figure out how the codebase is structured."
        ),
        verbose=True,
        allow_delegation=False,
        tools=[list_directory, read_file],
        llm=get_llm(role="tool"),
        respect_context_window=False,
    )

def create_analyzer_agent():
    """Analyzer reads source files and detects bugs — needs tool-calling support."""
    return Agent(
        role='Code Analyzer',
        goal='Deep dive into specific files and modules to find logic errors, syntax issues, or bugs based on the intended project behavior.',
        backstory=(
            'You are a meticulous senior software engineer. You notice every tiny detail '
            'and bug that others miss. You collaborate to figure out if the project works '
            'as the developer intends.'
        ),
        verbose=True,
        allow_delegation=False,
        tools=[list_directory, read_file],
        llm=get_llm(role="tool"),
        respect_context_window=False,
    )

def create_liaison_agent():
    """Liaison writes the final report — no tool use, qwen2.5:3b is fast & sufficient."""
    return Agent(
        role='Copilot Liaison Reporter',
        goal=(
            'Compile all findings and errors into a clean, highly structured Markdown report. '
            'Perform a quantitative summary: count total errors, classify by severity '
            '(Critical, Major, Minor), and calculate a Project Health Score (0-100).'
        ),
        backstory=(
            'You are a technical writer and senior project manager. You excel at turning '
            'technical bug reports into actionable project summaries. You categorize errors '
            'by severity, estimate technical debt in hours, and provide a definitive Health '
            'Score. You produce structured reports that include a JSON metadata section for '
            'automated processing.'
        ),
        verbose=True,
        allow_delegation=False,
        llm=get_llm(role="report"),
        respect_context_window=False,
    )
