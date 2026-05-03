# Implementation Plan - Enhanced Dual-Format Reporting

The goal is to enhance the Healium analysis output by providing a professional PDF report alongside the existing Markdown report. The PDF will include error counts, time estimates for fixes, and visual graphs showing the distribution of issues.

## User Review Required

> [!IMPORTANT]
> The PDF generation will rely on `fpdf2` and `matplotlib`. I will need to install these dependencies.
> The LLM will be instructed to provide metadata (counts and categories) in a structured format within the Markdown to enable accurate parsing for the PDF and graphs.

## Proposed Changes

### Dependencies
#### [MODIFY] [requirements.txt](file:///c:/Users/yashw/Desktop/Healium/requirements.txt)
- Add `fpdf2` for PDF generation.
- Add `matplotlib` for graph generation.

---

### Agent & Task Logic
#### [MODIFY] [tasks.py](file:///c:/Users/yashw/Desktop/Healium/tasks.py)
- Update `create_report_generation_task` to require a structured metadata section at the end of the report. This section will include:
    - Total error count.
    - Categorized error counts (Logic, Syntax, Security, Performance, etc.).
    - Total time estimate to fix all issues (in hours).

#### [MODIFY] [agents.py](file:///c:/Users/yashw/Desktop/Healium/agents.py)
- Update `create_liaison_agent`'s goal/backstory to emphasize quantitative analysis (counting and estimating).

---

### Report Generation Utility
#### [NEW] [report_gen.py](file:///c:/Users/yashw/Desktop/Healium/report_gen.py)
- Create a utility to:
    1. Parse the Markdown report for the structured metadata.
    2. Generate a pie chart or bar graph of error categories using `matplotlib`.
    3. Construct a PDF using `fpdf2` that includes:
        - Project Overview.
        - Summary Statistics (Total Errors, Time Estimate).
        - The generated graph.
        - The detailed issue list from the Markdown.

---

### Main Execution Flow
#### [MODIFY] [main.py](file:///c:/Users/yashw/Desktop/Healium/main.py)
- Import the new `report_gen` utility.
- After the crew finishes `kickoff()`, pass the result to the PDF generator.
- Update the completion message to notify the user about both the `.md` and `.pdf` reports.

## Verification Plan

### Automated Tests
- Run the system on a sample repository (e.g., Healium itself) and verify:
    - `copilot_report.md` contains the new metadata section.
    - `healium_analysis_report.pdf` is generated.
    - The PDF contains the expected text, statistics, and graph image.

### Manual Verification
- Open the generated PDF to check formatting, alignment, and graph clarity.
- Check the time estimates and error counts for logical consistency with the Markdown content.
