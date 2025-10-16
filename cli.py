"""
cli.py
Simple command-line interface to the planner.
"""
import argparse
from planner import generate_advanced_plan, export_plan_csv, export_plan_ics, export_gantt_png
import datetime, os

def main():
    parser = argparse.ArgumentParser(description="Smart Task Planner (Advanced)")
    parser.add_argument("--goal", "-g", required=True, help="Goal text, e.g. 'Launch a product in 2 weeks'")
    parser.add_argument("--start", "-s", help="Start date (YYYY-MM-DD). Defaults to today.")
    parser.add_argument("--out", "-o", help="Output folder", default="output_plan")
    parser.add_argument("--max-days", type=int, help="Force a maximum total timeline in days")
    args = parser.parse_args()

    start = None
    if args.start:
        start = datetime.date.fromisoformat(args.start)
    plan = generate_advanced_plan(args.goal, start_date=start, max_days=args.max_days)
    out = args.out
    os.makedirs(out, exist_ok=True)
    csvp = os.path.join(out, "plan.csv")
    ics = os.path.join(out, "plan.ics")
    gantt = os.path.join(out, "gantt.png")
    export_plan_csv(plan, csvp)
    export_plan_ics(plan, ics)
    export_gantt_png(plan, gantt)
    print(f"Exported CSV -> {csvp}")
    print(f"Exported ICS -> {ics}")
    print(f"Exported Gantt -> {gantt}")

if __name__ == "__main__":
    main()
