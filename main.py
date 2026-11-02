"""Check database backups against their RPO: breached or still safe.

Usage: python3 main.py backups.csv [--now 2026-10-31T12:00:00]
CSV columns: database,last_backup,rpo_hours (ISO timestamps).
Age over RPO is BREACHED; age over 80% of RPO is AT RISK; else OK.
"""
import argparse, csv, sys
from datetime import datetime


def status(last_backup, rpo_hours, now):
    age_hours = (now - datetime.fromisoformat(last_backup)).total_seconds() / 3600
    if age_hours > rpo_hours:
        return "BREACHED", round(age_hours, 1)
    if age_hours > 0.8 * rpo_hours:
        return "AT RISK", round(age_hours, 1)
    return "OK", round(age_hours, 1)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    parser.add_argument("--now", default=None)
    args = parser.parse_args(argv)
    now = datetime.fromisoformat(args.now) if args.now else datetime.now()
    breached = 0
    with open(args.path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            verdict, age = status(row["last_backup"], float(row["rpo_hours"]), now)
            if verdict == "BREACHED":
                breached += 1
            print(f"{row['database']}: {verdict} (last backup {age}h ago, RPO {row['rpo_hours']}h)")
    print(f"{breached} database(s) breaching RPO.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
