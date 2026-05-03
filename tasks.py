from crewai import Task

def create_architecture_analysis_task(agent, repo_path, developer_prompt):
    return Task(
        description=f"""
        Analyze the repository located at '{repo_path}'.
        The developer has described the project as follows: "{developer_prompt}".
        
        1. Use your tools to list the directory contents and read the key files (like README, main application files, package.json or requirements.txt).
        2. Identify the main modules and architecture.
        3. Create a brief summary of how the project is structured and what the analyzers should focus on.
        """,
        expected_output="A summary of the project structure and a list of key files that need to be analyzed for bugs.",
        agent=agent
    )

def create_code_analysis_task(agent, architecture_summary_placeholder):
    return Task(
        description="""
        Based on the architecture summary provided by the Architect: 
        
        1. Read the contents of the key files identified.
        2. Analyze the code for logical errors, syntax issues, or deviations from the intended behavior described in the developer's prompt.
        3. Identify any issues, edge cases, or bugs. Focus on tiny little details.
        """,
        expected_output="A detailed list of errors, bugs, or improvements found in the codebase, including file names and specific code snippets.",
        agent=agent
    )

def create_report_generation_task(agent):
    return Task(
        description="""
        Take the list of errors and bugs discovered by the Code Analyzer.
        Format these findings into a "Copilot-Ready" Markdown report.
        The report MUST include:
        - A brief summary of the issues found.
        - For each issue: the specific file name, the problematic code snippet, an explanation of the error, and a prompt suggestion that the developer can copy-paste to an AI Copilot to fix it.
        """,
        expected_output="A complete Markdown formatted string that serves as the final error report.",
        agent=agent,
        output_file='copilot_report.md'
    )
