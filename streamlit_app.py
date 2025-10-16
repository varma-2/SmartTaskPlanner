import streamlit as st
from planner import generate_advanced_plan, export_plan_csv, export_gantt_png, export_effort_pie, export_dependency_graph
from db import init_db, save_plan
import datetime, os

init_db()
st.set_page_config(page_title="Smart Task Planner", layout="centered")
st.title("🧠 Smart Task Planner")

with st.form("goal_form"):
    goal = st.text_input("Enter your goal", value="")
    start = st.date_input("Start date", value=datetime.date.today())
    max_days = st.number_input("Max allowed days (0=auto)", min_value=0, value=0)
    submitted = st.form_submit_button("Generate Plan")

if submitted and goal.strip():
    plan = generate_advanced_plan(goal, start_date=start, max_days=None if max_days==0 else max_days)

    st.subheader("Plan Summary")
    rows = []
    for t in plan.tasks:
        rows.append({
            "ID": t.id,
            "Task": t.title,
            "Duration (days)": t.duration_days,
            "Start": t.earliest_start.isoformat(),
            "End": t.latest_end.isoformat(),
            "Depends on": ",".join(map(str,t.depends_on))
        })
    st.table(rows)

    outdir = "streamlit_output"
    os.makedirs(outdir, exist_ok=True)
    csvp = os.path.join(outdir,"plan.csv")
    gantt = os.path.join(outdir,"gantt.png")
    pie = os.path.join(outdir,"effort.png")
    dep_graph = os.path.join(outdir,"dependency.png")

    export_plan_csv(plan, csvp)
    export_gantt_png(plan, gantt)
    export_effort_pie(plan, pie)
    export_dependency_graph(plan, dep_graph)

    st.success(f"Exported CSV -> {csvp}")
    st.image(gantt, caption="Gantt Chart")
    st.image(pie, caption="Task Effort Distribution")
    st.image(dep_graph, caption="Task Dependency Graph")

    pid = save_plan(plan)
    st.info(f"Saved project to local DB (id={pid})")
