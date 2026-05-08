# 🚀 Healium: Cooperative Agentic Testing System

Healium is an automated, multi-agent system designed to analyze software repositories, identify logic errors, and generate actionable reports for AI Copilots (like GitHub Copilot or ChatGPT) to fix.

## 🌟 Features

-   **Multi-Agent Architecture:** Uses specialized agents (Architect, Analyzer, Liaison) to provide deep code insights.
-   **Local & Cloud LLM Support:** 
    -   **Local:** Optimized for [Ollama](https://ollama.com/) (default: `qwen2.5:3b`).
    -   **Cloud:** Supports Groq (Llama 3.3 70B), OpenAI (GPT-4o), and Google (Gemini 1.5 Pro).
-   **GUI & CLI Modes:** Run tests via a sleek web interface or directly from your terminal.
-   **Copilot-Ready Reports:** Generates structured Markdown reports designed for seamless bug fixing.

## 🛠️ Installation

1.  **Clone the Repository:**
    ```bash
    git clone <repository-url>
    cd Healium
    ```

2.  **Set Up a Virtual Environment:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # Windows
    source venv/bin/activate  # macOS/Linux
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt

##Visit the reports folder to check the sample reports. And better understand what is happening in Healium. 
## Don't forget to use the prompt_guide for better understanding of how to use the Healium.
## Don't forget to Star the repo if you liked it.
    ```

## ⚙️ Configuration

Create a `.env` file in the root directory by copying `.env.example`:
```bash
cp .env.example .env
```

### Option A: Local (Ollama)
Ensure Ollama is running and you have the model installed:
```bash
ollama pull qwen2.5:3b
```
The system will default to Ollama if no API keys are found.

### Option B: Cloud (Groq/OpenAI/Google)
Add your API keys to the `.env` file:
```env
GROQ_API_KEY="your_groq_key"
OPENAI_API_KEY="your_openai_key"
GOOGLE_API_KEY="your_google_key"
```

## 🚀 Usage

### Command Line Interface (CLI)
Run the main script and follow the prompts:
```bash
python main.py
```

### Graphical User Interface (GUI)
Start the Healium server in GUI mode:
```bash
python main.py --gui
```
Then open your browser at `http://localhost:8000`.

## 📁 Project Structure

-   `main.py`: Entry point for both CLI and GUI modes.
-   `agents.py`: Definitions for the Project Architect, Code Analyzer, and Liaison Reporter agents.
-   `tasks.py`: Structured tasks for architecture analysis and report generation.
-   `api.py`: FastAPI backend for real-time log streaming and GUI interaction.
-   `tools.py`: Specialized tools for repository traversal and file analysis.
-   `gui/`: Frontend assets for the web interface.

## 📄 License
Free For All. Fork & Share the code.
