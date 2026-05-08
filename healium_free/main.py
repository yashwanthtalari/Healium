import os
import sys
import asyncio
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')
from dotenv import load_dotenv
from crewai import Crew, Process
from agents import create_architect_agent, create_analyzer_agent, create_liaison_agent
from tasks import create_architecture_analysis_task, create_code_analysis_task, create_report_generation_task
from report_gen import create_pdf_report

# Load environment variables
load_dotenv()

# GUI Integration
from api import app, LogStream, manager
import threading
import uvicorn

def run_healium_test(repo_path: str, developer_prompt: str):
    print(f"Starting Healium Agentic Test on: {repo_path}")
    print(f"Developer Intent: {developer_prompt}\n")

    # 1. Initialize Agents
    try:
        architect = create_architect_agent()
        analyzer = create_analyzer_agent()
        liaison = create_liaison_agent()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        sys.exit(1)

    # 2. Create Tasks
    md_report_path = os.path.join(repo_path, 'copilot_report.md')
    pdf_report_path = os.path.join(repo_path, 'healium_analysis_report.pdf')
    
    arch_task = create_architecture_analysis_task(architect, repo_path, developer_prompt)
    analysis_task = create_code_analysis_task(analyzer, "Use the output of the architecture task.")
    report_task = create_report_generation_task(liaison, output_file=md_report_path)

    # 3. Form the Crew
    healium_crew = Crew(
        agents=[architect, analyzer, liaison],
        tasks=[arch_task, analysis_task, report_task],
        process=Process.sequential, # Sequential execution: Arch -> Analyzer -> Liaison
        verbose=True,
        memory=False,  # Disable memory to avoid hidden OpenAI embedding calls
        share_crew=False  # Disable telemetry
    )

    # 4. Kickoff the testing process
    print("Initiating Agentic Testing...")
    result = healium_crew.kickoff()
    
    print("\n==============================================")
    print("Healium Testing Complete!")
    print(f"The final report has been saved to: {md_report_path}")
    
    # Generate PDF report
    try:
        create_pdf_report(str(result), output_filename=pdf_report_path)
        print(f"A professional PDF summary has been generated: {pdf_report_path}")
    except Exception as e:
        print(f"Warning: Failed to generate PDF report: {e}")
        
    print("==============================================\n")
    
    # Broadcast completion to GUI
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.run_coroutine_threadsafe(
                manager.broadcast({"type": "log", "data": "TESTING COMPLETE. Report generated."}), 
                loop
            )
    except:
        pass

def start_gui():
    # Use a custom config to avoid logging conflicts with our LogStream
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=None)

if __name__ == "__main__":
    # Ensure event loop exists for broadcast
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

    if "--gui" in sys.argv:
        print("Starting Healium in GUI mode...")
        # Start log redirector
        stream = LogStream()
        
        @app.post("/api/start")
        async def start_test_endpoint(data: dict):
            repo_path = data.get("repo_path")
            prompt = data.get("prompt")
            if not repo_path or not prompt:
                return {"status": "error", "message": "Missing repo_path or prompt"}
            
            # Start test in background thread
            t = threading.Thread(target=run_healium_test, args=(repo_path, prompt))
            t.start()
            return {"status": "success", "message": "Testing started"}
            
        print("GUI available at: http://localhost:8000")
        
        # Run uvicorn on the main thread in GUI mode
        start_gui()
    else:
        print("Welcome to Healium Cooperative Agentic Testing System")
        target_repo = input("Enter the absolute path to the repository you want to test: ").strip()
        project_prompt = input("Enter a short prompt describing what the project needs to do: ").strip()
        
        if os.path.exists(target_repo):
            run_healium_test(target_repo, project_prompt)
        else:
            print(f"Error: The path '{target_repo}' does not exist.")
