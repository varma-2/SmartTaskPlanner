# Smart Task Planner 


It provides:

- Domain-adaptive heuristic task generation (product/content/research/generic)
- Optional local LLM hook (you can plug a `model_fn` using Hugging Face `transformers` if you run a local model)
- Dependency validation (topological sort)
- Timeline estimation and forward scheduling
- Exporters: CSV, ICS (calendar), Gantt PNG
- SQLite storage for projects & tasks
- Optional Streamlit frontend for easy interaction


## Files

planner.py — Core planner logic

cli.py — Command-line interface (exports CSV, ICS, Gantt)

streamlit_app.py — Optional UI (streamlit run streamlit_app.py)

db.py — SQLite persistence

utils.py — Small helpers

requirements.txt — Python dependencies

## How this version is unique / advanced

Domain-adaptive task clusters selected by parsing the goal

Smart scaling of task durations to match requested deadlines

Local LLM hook pattern for users who can run a model locally (no third-party API calls required)

Exports to calendar (ICS) and a Gantt chart for visual planning

Simple local DB to save and revisit plans

## Architecture
                +------------------+
                |   User Input     |
                | CLI / Streamlit  |
                +--------+---------+
                         |
                         v
                 +----------------+
                 | Planner Module |
                 | (planner.py)   |
                 +--------+-------+
                          |
    +---------------------+-------------------+
    |                                         |
    v                                         v
+-----------+                           +-----------+
| Task &    |                           | Timeline  |
| Plan      |                           | Scheduler |
| Classes   |                           | & Forward |
+-----------+                           | Scheduling|
                                        +-----------+
                          |
                          v
                 +----------------+
                 | Exporters      |
                 | CSV, ICS, PNG  |
                 +----------------+
                          |
                          v
                 +----------------+
                 | SQLite DB      |
                 | db.py          |
                 +----------------+
                          |
                          v
                 +----------------+
                 | Optional LLM   |
                 | Integration    |
                 +----------------+

## Quick start (local)

Create and activate a python virtual environment:

python -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate


Install dependencies:

pip install -r requirements.txt


Run CLI example:

python cli.py --goal "Launch a product in 2 weeks" --out myplan


Run Streamlit UI (optional):

streamlit run streamlit_app.py

## Local LLM Integration

You can integrate a local Hugging Face model by providing a model_fn(prompt: str) -> str function. The model should return JSON-like structured tasks.

Example prompt:

Goal: "Launch a new e-commerce website in 4 weeks"
Requirements:
- Break the goal into actionable tasks
- Provide estimated duration in days
- Specify dependencies
- Return JSON with: title, duration_days, depends_on, notes


Example JSON output:

[
  {"title": "Define website requirements", "duration_days": 2, "depends_on": [], "notes": ""},
  {"title": "Design UI/UX", "duration_days": 4, "depends_on": [0], "notes": ""},
  {"title": "Develop frontend", "duration_days": 7, "depends_on": [1], "notes": ""},
  {"title": "Develop backend", "duration_days": 7, "depends_on": [1], "notes": ""},
  {"title": "Testing & QA", "duration_days": 3, "depends_on": [2,3], "notes": ""},
  {"title": "Launch website", "duration_days": 1, "depends_on": [4], "notes": ""}
]

## Visualizations

Gantt Chart: Timeline view of tasks

Effort Pie Chart: Shows % effort per task

Dependency Graph: Directed graph showing task dependencies

All exports are automatically saved to the output folder.

## License

MIT
