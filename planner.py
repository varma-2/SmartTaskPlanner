from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict
import datetime
import csv
import os

# -------------------------
# Data classes
# -------------------------
@dataclass
class Task:
    id: int
    title: str
    duration_days: int
    earliest_start: Optional[datetime.date] = None
    latest_end: Optional[datetime.date] = None
    depends_on: List[int] = field(default_factory=list)
    notes: str = ""

    def to_dict(self):
        d = asdict(self)
        if self.earliest_start: d["earliest_start"] = self.earliest_start.isoformat()
        if self.latest_end: d["latest_end"] = self.latest_end.isoformat()
        return d

@dataclass
class Plan:
    goal: str
    created_on: datetime.date
    tasks: List[Task] = field(default_factory=list)
    start_date: Optional[datetime.date] = None

    def to_dict(self):
        return {
            "goal": self.goal,
            "created_on": self.created_on.isoformat(),
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "tasks": [t.to_dict() for t in self.tasks],
        }

# -------------------------
# Utilities
# -------------------------
def parse_duration_from_goal(goal_text: str, default_days: int = 14) -> int:
    import re
    text = goal_text.lower()
    m = re.search(r"in (\d+)\s*days?", text)
    if m: return int(m.group(1))
    m = re.search(r"in (\d+)\s*weeks?", text)
    if m: return int(m.group(1)) * 7
    m = re.search(r"by (\d{4}-\d{2}-\d{2})", text)
    if m:
        try:
            d = datetime.date.fromisoformat(m.group(1))
            return max(1, (d - datetime.date.today()).days)
        except: return default_days
    return default_days

# -------------------------
# Heuristic Task Generator
# -------------------------
def heuristic_task_templates(goal_text: str) -> List[Dict]:
    text = goal_text.lower()
    clusters = []
    if any(k in text for k in ["product","launch","mvp","release"]):
        clusters = [
            {"title":"Clarify goals & metrics", "effort":1},
            {"title":"Market research & user interviews", "effort":2},
            {"title":"Define MVP scope", "effort":1},
            {"title":"Prototype / Design", "effort":2},
            {"title":"MVP Development", "effort":4},
            {"title":"Testing & QA with users", "effort":2},
            {"title":"Marketing & launch prep", "effort":2},
            {"title":"Launch & monitor metrics", "effort":1},
        ]
    elif any(k in text for k in ["write","blog","article","ebook","post"]):
        clusters = [
            {"title":"Define outline & audience", "effort":1},
            {"title":"Research and references", "effort":2},
            {"title":"Write first draft", "effort":3},
            {"title":"Edit and proofread", "effort":1},
            {"title":"Design cover/images", "effort":1},
            {"title":"Publish & promote", "effort":2},
        ]
    elif any(k in text for k in ["research","paper","study","experiment"]):
        clusters = [
            {"title":"Define hypothesis and scope", "effort":1},
            {"title":"Literature review", "effort":3},
            {"title":"Design experiment / method", "effort":2},
            {"title":"Collect data", "effort":4},
            {"title":"Analyze and write results", "effort":3},
            {"title":"Submit / share findings", "effort":1},
        ]
    else:
        clusters = [
            {"title":"Clarify the goal", "effort":1},
            {"title":"Break into key milestones", "effort":2},
            {"title":"Create deliverables", "effort":3},
            {"title":"Implement first deliverable", "effort":3},
            {"title":"Test & iterate", "effort":2},
            {"title":"Finalize & deliver", "effort":1},
        ]
    return clusters

# -------------------------
# Build Plan
# -------------------------
def build_plan_from_goal(goal_text: str, start_date: Optional[datetime.date]=None, max_days: Optional[int]=None) -> Plan:
    if start_date is None: start_date = datetime.date.today()
    total_days = parse_duration_from_goal(goal_text)
    if max_days: total_days = min(total_days, max_days)

    templates = heuristic_task_templates(goal_text)
    efforts = [t["effort"] for t in templates]
    total_effort = sum(efforts)
    scaled = [max(1, round(e / total_effort * total_days)) for e in efforts]

    diff = total_days - sum(scaled)
    idx = 0
    while diff != 0:
        scaled[idx % len(scaled)] += 1 if diff>0 else -1
        idx +=1
        diff = total_days - sum(scaled)

    tasks = []
    for i, tpl in enumerate(templates):
        t = Task(
            id=i+1,
            title=tpl["title"],
            duration_days=scaled[i],
            depends_on=[i] if i>0 else [],
        )
        tasks.append(t)

    plan = Plan(goal=goal_text, created_on=datetime.date.today(), tasks=tasks, start_date=start_date)

    cur = start_date
    for t in plan.tasks:
        t.earliest_start = cur
        t.latest_end = cur + datetime.timedelta(days=t.duration_days-1)
        cur = t.latest_end + datetime.timedelta(days=1)

    return plan

# -------------------------
# Exporters
# -------------------------
def export_plan_csv(plan: Plan, path: str):
    keys = ["id","title","duration_days","earliest_start","latest_end","depends_on","notes"]
    with open(path,"w",newline="",encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for t in plan.tasks:
            writer.writerow({
                "id": t.id,
                "title": t.title,
                "duration_days": t.duration_days,
                "earliest_start": t.earliest_start.isoformat() if t.earliest_start else "",
                "latest_end": t.latest_end.isoformat() if t.latest_end else "",
                "depends_on": ",".join(map(str,t.depends_on)),
                "notes": t.notes
            })

def export_gantt_png(plan: Plan, path: str):
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    labels = [t.title for t in plan.tasks]
    starts = [(t.earliest_start - plan.start_date).days for t in plan.tasks]
    durations = [t.duration_days for t in plan.tasks]
    y = range(len(plan.tasks))

    colors = plt.cm.tab20.colors
    fig, ax = plt.subplots(figsize=(10, 0.8*len(plan.tasks)+1))
    for i, (s,d) in enumerate(zip(starts,durations)):
        ax.barh(y[i], d, left=s, color=colors[i%len(colors)], edgecolor="black")
        ax.text(s + d/2, y[i], f"{d}d", va='center', ha='center', color='white', fontsize=8, fontweight='bold')

    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Days from start")
    ax.invert_yaxis()
    ax.grid(axis="x")
    plt.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)

def export_effort_pie(plan: Plan, path: str):
    import matplotlib.pyplot as plt
    labels = [t.title for t in plan.tasks]
    durations = [t.duration_days for t in plan.tasks]
    colors = plt.cm.tab20.colors
    fig, ax = plt.subplots(figsize=(6,6))
    ax.pie(durations, labels=labels, autopct="%1.1f%%", colors=colors)
    ax.set_title("Task Effort Distribution")
    plt.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)

def export_dependency_graph(plan: Plan, path: str):
    """
    Visualize task dependencies as a directed graph using NetworkX.
    """
    import matplotlib.pyplot as plt
    import networkx as nx

    G = nx.DiGraph()
    for t in plan.tasks:
        G.add_node(t.id, label=t.title)
        for dep in t.depends_on:
            if dep > 0:
                G.add_edge(dep, t.id)

    pos = nx.spring_layout(G, seed=42)
    labels = {t.id: t.title for t in plan.tasks}

    plt.figure(figsize=(10, max(3, len(plan.tasks)//2)))
    nx.draw(G, pos, with_labels=True, labels=labels, node_size=2500,
            node_color='skyblue', font_size=8, font_weight='bold',
            arrowsize=20, arrowstyle='-|>')
    plt.title("Task Dependency Graph")
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()  # <- remove fig, just close current figure


# -------------------------
# Public function
# -------------------------
def generate_advanced_plan(goal_text: str, start_date: Optional[datetime.date]=None, max_days: Optional[int]=None) -> Plan:
    return build_plan_from_goal(goal_text, start_date=start_date, max_days=max_days)
