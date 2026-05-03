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

def create_report_generation_task(agent, output_file='copilot_report.md'):
    return Task(
        description="""
        Take the list of errors and bugs discovered by the Code Analyzer.
        Format these findings into a "Copilot-Ready" Markdown report.
        The report MUST include:
        1. A brief summary of the issues found.
        2. For each issue: the specific file name, the problematic code snippet, an explanation of the error, its severity (Critical, Major, Minor), and a prompt suggestion for a fix.
        
        CRITICAL: At the very end of the report, you MUST include a "REPORT_METADATA" section inside a JSON code block.
        The JSON must contain:
        - "total_errors": (integer) Total number of bugs/issues found.
        - "estimated_fix_time": (string) Total time needed to fix all issues.
        - "health_score": (integer) Score from 0 to 100 based on findings.
        - "technical_debt": (string) "High", "Medium", or "Low".
        - "error_distribution": (object) Counts by category (Logic, Syntax, etc.).
        - "severity_distribution": (object) Counts by severity (Critical, Major, Minor).
        
        Example Metadata Format:
        ```json
        {
          "total_errors": 5,
          "estimated_fix_time": "2 hours",
          "health_score": 85,
          "technical_debt": "Medium",
          "error_distribution": {
            "Logic": 3,
            "Syntax": 2
          },
          "severity_distribution": {
            "Critical": 1,
            "Major": 2,
            "Minor": 2
          }
        }
        ```
        """,
        expected_output="A complete Markdown formatted string that serves as the final error report, including the JSON metadata block at the end.",
        agent=agent,
        output_file=output_file
    )
