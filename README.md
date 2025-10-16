# Smart Task Planner — Advanced (Local, No API)

This is an **advanced, self-contained** Smart Task Planner designed to run locally without external APIs.  
It provides:

- Domain-adaptive heuristic task generation (product/content/research/generic)
- Optional local LLM hook (you can plug a `model_fn` using Hugging Face `transformers` if you run a local model)
- Dependency validation (topological sort)
- Timeline estimation and forward scheduling
- Exporters: CSV, ICS (calendar), Gantt PNG
- SQLite storage for projects & tasks
- Optional Streamlit frontend for easy interaction

## Files
- `planner.py` — Core planner logic
- `cli.py` — Command-line interface (exports CSV, ICS, Gantt)
- `streamlit_app.py` — Optional UI (`streamlit run streamlit_app.py`)
- `db.py` — SQLite persistence
- `utils.py` — Small helpers
- `requirements.txt` — Python dependencies

## How this version is unique / advanced
- Domain-adaptive task clusters selected by parsing the goal.
- Smart scaling of task durations to match requested deadline.
- Local LLM hook pattern for users who can run a model locally (no third-party API calls required).
- Exports to calendar (ICS) and a Gantt chart for visual planning.
- Simple local DB to save and revisit plans.

## Quick start (local)
1. Create and activate a python venv.
2. Install requirements:
```bash
pip install -r requirements.txt
```
3. CLI usage example:
```bash
python cli.py --goal "Launch a product in 2 weeks" --out myplan
```
4. Run Streamlit UI (optional):
```bash
streamlit run streamlit_app.py
```

## Notes on local LLM usage
If you have a local HF model, you can integrate by passing a `model_fn` that accepts a prompt and returns text. The code will attempt to parse JSON from the model output.

## License
MIT
