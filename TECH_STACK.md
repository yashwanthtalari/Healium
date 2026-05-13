#  Healium: Tech Stack & Technology Report

Healium is a sophisticated, multi-agent software testing and analysis system. This report outlines the various layers and technologies that power the platform.

---

##  Core Backend & Logic
The heart of Healium is built on a Python-based multi-agent architecture.

*   **Language:** Python 3.10+
*   **Agent Framework:** [CrewAI](https://www.crewai.com/) (v0.28.8) - Manages the orchestration, collaboration, and delegation between specialized AI agents.
*   **LLM Orchestration:** [LangChain](https://www.langchain.com/) - Provides the integration layer for various LLM providers (Google GenAI, OpenAI, Groq, Community).
*   **Task Management:** Custom-defined tasks (`tasks.py`) that structure the workflow from architecture analysis to final report generation.

---

##  Intelligence Layer (LLM Support)
Healium is designed to be model-agnostic, supporting both local and cloud-based intelligence.

### **Local Models**
*   **Ollama:** Primary local provider (default model: `qwen2.5:3b`). This ensures data privacy and offline capability.

### **Cloud Models**
*   **Google AI:** Gemini 1.5 Pro integration.
*   **OpenAI:** GPT-4o integration.
*   **Groq:** Llama 3.3 70B (High-speed inference).

---

##  API & Networking
The bridge between the backend logic and the user interface.

*   **Web Framework:** [FastAPI](https://fastapi.tiangolo.com/) - A modern, high-performance web framework for building APIs.
*   **ASGI Server:** [Uvicorn](https://www.uvicorn.org/) - Handles the lightning-fast delivery of the web application.
*   **Real-time Streaming:** [WebSockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API) - Used for streaming live agent logs and activity directly to the GUI console.

---

##  Frontend (Graphical User Interface)
A premium, responsive "Glassmorphic" web interface for managing tests.

*   **Structure:** Semantic HTML5.
*   **Styling:** Modern CSS3 featuring:
    *   **Glassmorphism:** Frosted glass effects for containers.
    *   **Dynamic Backgrounds:** Animated CSS blobs for a high-end aesthetic.
    *   **Responsive Design:** Optimized for various screen sizes.
*   **Interactivity:** Vanilla JavaScript (ES6+) for DOM manipulation, WebSocket handling, and UI state management.
*   **Typography:** [Outfit](https://fonts.google.com/specimen/Outfit) via Google Fonts (Modern, clean sans-serif).

---

##  Reporting & Utilities
Tools used for generating the final analysis output.

*   **PDF Generation:** `fpdf2` - Used to compile analysis results into professional, downloadable reports.
*   **Data Visualization:** `matplotlib` - (Planned/Used) for generating visual representations of code metrics and error distributions.
*   **Environment Management:** `python-dotenv` - For secure handling of API keys and configuration.

---

##  Project Structure Overview
*   `main.py`: Dual-mode entry point (CLI/GUI).
*   `agents.py`: Logic for specialized agents (Architect, Analyzer, Liaison).
*   `api.py`: Backend server logic and WebSocket endpoints.
*   `tools.py`: Custom file-system and repository traversal tools.
*   `gui/`: Static assets for the web interface.

---
*Report generated on: 2026-05-13*
