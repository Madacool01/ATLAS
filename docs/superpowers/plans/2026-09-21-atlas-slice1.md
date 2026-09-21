# ATLAS Slice-1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Local Python CLI reads questions.csv + scores.csv and prints per-topic mastery for class and each student plus weakest-topics list.

**Architecture:** Pure-stdlib Python, CSV in / text out. Multi-topic questions count full points for each listed topic (simplest, documented). No external calls, no names — student_id aliases only.

**Tech Stack:** Python 3.14 stdlib only (csv, json, argparse, pathlib), unittest via `python -m unittest`, no third-party deps.

## Global Constraints

- Student scores stay local; student_id aliases only, never real names.
- No external AI/API calls in Slice-1 (Groq comes in Slice-2).
- Smallest unit is question tied to topic(s); topics split by `;` in questions.csv.
- Teacher-defined thresholds from thresholds.json drive labels, not hard-coded meanings.
- Wide scores.csv format: one row per student, one column per question_id.
- YAGNI: stdlib only, no web UI, no DB in Slice-1.

---

### Task 1: Loader + example data

**Files:**
- Create: `atlas/__init__.py`
- Create: `atlas/loader.py`
- Create: `data/example1/questions.csv`
- Create: `data/example1/scores.csv`
- Create: `data/example1/thresholds.json`
- Test: `tests/test_loader.py`

**Interfaces:**
- Consumes: CSV files on disk (paths as strings).
- Produces: `load_questions(path: str) -> dict[str, dict]` with `{qid: {"max_points": float, "topics": list[str]}}`; `load_scores(path: str) -> tuple[list[str], dict[str, dict[str, float]]]` returning `(question_ids, {student_id: {qid: points}})`; `load_thresholds(path: str) -> dict` with `{"failed_below": float, "needs_practice_below": float}`.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_loader.py
import pathlib
import unittest

from atlas.loader import load_questions, load_scores, load_thresholds


class TestLoader(unittest.TestCase):
    def test_loads_example1(self):
        base = pathlib.Path("data/example1")
        questions = load_questions(str(base / "questions.csv"))
        self.assertEqual(questions["Q1"]["max_points"], 10)
        self.assertEqual(questions["Q1"]["topics"], ["Fractions"])
        self.assertEqual(questions["Q3"]["topics"], ["Fractions", "Equations"])
        qids, scores = load_scores(str(base / "scores.csv"))
        self.assertEqual(qids, ["Q1", "Q2", "Q3"])
        self.assertEqual(scores["S01"]["Q1"], 8)
        thresholds = load_thresholds(str(base / "thresholds.json"))
        self.assertEqual(thresholds["failed_below"], 50)
        self.assertEqual(thresholds["needs_practice_below"], 75)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_loader -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'atlas'" or "No such file".

- [ ] **Step 3: Write minimal implementation + example data**

```python
# atlas/__init__.py
"""ATLAS Slice-1: local topic mastery calculator."""
```

```python
# atlas/loader.py
"""Load questions, scores, thresholds from CSV/JSON."""
import csv
import json


def load_questions(path: str) -> dict:
    questions: dict = {}
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            qid = row["question_id"].strip()
            max_points = float(row["max_points"])
            topics = [t.strip() for t in row["topics"].split(";") if t.strip()]
            questions[qid] = {"max_points": max_points, "topics": topics}
    return questions


def load_scores(path: str) -> tuple:
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        qids = [c for c in fieldnames if c != "student_id"]
        scores: dict = {}
        for row in reader:
            sid = row["student_id"].strip()
            scores[sid] = {qid: float(row[qid]) for qid in qids}
    return qids, scores


def load_thresholds(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return {"failed_below": float(data["failed_below"]), "needs_practice_below": float(data["needs_practice_below"])}
```

```csv
# data/example1/questions.csv
question_id,max_points,topics
Q1,10,Fractions
Q2,10,Equations
Q3,10,Fractions;Equations
```

```csv
# data/example1/scores.csv
student_id,Q1,Q2,Q3
S01,8,5,6
S02,4,9,7
S03,10,6,9
```

```json
// data/example1/thresholds.json
{"failed_below": 50, "needs_practice_below": 75}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m unittest tests.test_loader -v`
Expected: PASS (1 test, OK).

- [ ] **Step 5: Commit**

```bash
git add atlas/__init__.py atlas/loader.py tests/test_loader.py data/example1/questions.csv data/example1/scores.csv data/example1/thresholds.json
git commit -m "feat: add CSV loader and example assessment"
```

### Task 2: Topic mastery math

**Files:**
- Create: `atlas/analytics.py`
- Test: `tests/test_analytics.py`

**Interfaces:**
- Consumes: `questions: dict` from `load_questions`, `scores: dict` from `load_scores`.
- Produces: `class_mastery(questions, scores) -> dict[str, float]` (topic -> 0-100 pct); `student_mastery(questions, scores) -> dict[str, dict[str, float]]` (sid -> topic -> pct); `weakest_topics(class_pct: dict) -> list[str]` sorted ascending by pct.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_analytics.py
import unittest

from atlas.analytics import class_mastery, student_mastery, weakest_topics


def sample():
    questions = {
        "Q1": {"max_points": 10, "topics": ["Fractions"]},
        "Q2": {"max_points": 10, "topics": ["Equations"]},
        "Q3": {"max_points": 10, "topics": ["Fractions", "Equations"]},
    }
    scores = {
        "S01": {"Q1": 8, "Q2": 5, "Q3": 6},
        "S02": {"Q1": 4, "Q2": 9, "Q3": 7},
        "S03": {"Q1": 10, "Q2": 6, "Q3": 9},
    }
    return questions, scores


class TestAnalytics(unittest.TestCase):
    def test_class_mastery(self):
        questions, scores = sample()
        result = class_mastery(questions, scores)
        # Fractions: earned (8+6)+(4+7)+(10+9)=44, possible 3*20=60 -> 73.33
        # Equations: earned (5+6)+(9+7)+(6+9)=42, possible 60 -> 70.0
        self.assertAlmostEqual(result["Fractions"], 73.333, places=2)
        self.assertAlmostEqual(result["Equations"], 70.0, places=2)

    def test_student_mastery(self):
        questions, scores = sample()
        result = student_mastery(questions, scores)
        # S01 Fractions: (8+6)/20=70.0, Equations: (5+6)/20=55.0
        self.assertAlmostEqual(result["S01"]["Fractions"], 70.0, places=2)
        self.assertAlmostEqual(result["S01"]["Equations"], 55.0, places=2)

    def test_weakest_sorted(self):
        self.assertEqual(weakest_topics({"Fractions": 73.3, "Equations": 70.0}), ["Equations", "Fractions"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_analytics -v`
Expected: FAIL with "No module named 'atlas.analytics'".

- [ ] **Step 3: Write minimal implementation**

```python
# atlas/analytics.py
"""Per-topic mastery math. Multi-topic questions count full points per topic."""


def _topic_totals(questions: dict, earned_map: dict) -> dict:
    totals: dict = {}
    for qid, q in questions.items():
        earned = float(earned_map.get(qid, 0))
        max_pts = float(q["max_points"])
        for topic in q["topics"]:
            entry = totals.setdefault(topic, {"earned": 0.0, "possible": 0.0})
            entry["earned"] += earned
            entry["possible"] += max_pts
    return totals


def class_mastery(questions: dict, scores: dict) -> dict:
    combined: dict = {}
    for sid_points in scores.values():
        for qid, pts in sid_points.items():
            combined[qid] = combined.get(qid, 0.0) + float(pts)
    n_students = max(len(scores), 1)
    totals: dict = {}
    for qid, q in questions.items():
        earned = combined.get(qid, 0.0)
        for topic in q["topics"]:
            entry = totals.setdefault(topic, {"earned": 0.0, "possible": 0.0})
            entry["earned"] += earned
            entry["possible"] += float(q["max_points"]) * n_students
    return {t: (v["earned"] / v["possible"] * 100 if v["possible"] else 0.0) for t, v in totals.items()}


def student_mastery(questions: dict, scores: dict) -> dict:
    out: dict = {}
    for sid, sid_points in scores.items():
        totals = _topic_totals(questions, sid_points)
        out[sid] = {t: (v["earned"] / v["possible"] * 100 if v["possible"] else 0.0) for t, v in totals.items()}
    return out


def weakest_topics(class_pct: dict) -> list:
    return sorted(class_pct, key=lambda t: class_pct[t])
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m unittest tests.test_analytics -v`
Expected: PASS (3 tests, OK).

- [ ] **Step 5: Commit**

```bash
git add atlas/analytics.py tests/test_analytics.py
git commit -m "feat: add per-topic mastery math"
```

### Task 3: CLI text report with teacher thresholds

**Files:**
- Create: `atlas/report.py`
- Create: `atlas/cli.py`
- Test: `tests/test_report.py`

**Interfaces:**
- Consumes: `class_pct: dict`, `per_student: dict`, `thresholds: dict`, `order: list[str]`.
- Produces: `label_for(pct: float, thresholds: dict) -> str` ("failed" / "needs practice" / "solid"); `render_text(class_pct, per_student, thresholds, order) -> str`; CLI `python -m atlas.cli data/example1` prints report to stdout.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_report.py
import unittest

from atlas.report import label_for, render_text


class TestReport(unittest.TestCase):
    def test_labels_use_teacher_thresholds(self):
        th = {"failed_below": 50, "needs_practice_below": 75}
        self.assertEqual(label_for(40, th), "failed")
        self.assertEqual(label_for(70, th), "needs practice")
        self.assertEqual(label_for(80, th), "solid")

    def test_render_contains_weakest(self):
        class_pct = {"Fractions": 73.33, "Equations": 70.0}
        per_student = {"S01": {"Fractions": 70.0, "Equations": 55.0}}
        th = {"failed_below": 50, "needs_practice_below": 75}
        text = render_text(class_pct, per_student, th, ["Equations", "Fractions"])
        self.assertIn("Equations", text)
        self.assertIn("70.0%", text)
        self.assertIn("weakest", text.lower())


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_report -v`
Expected: FAIL with "No module named 'atlas.report'".

- [ ] **Step 3: Write minimal implementation**

```python
# atlas/report.py
"""Text report using teacher-defined thresholds."""


def label_for(pct: float, thresholds: dict) -> str:
    if pct < float(thresholds["failed_below"]):
        return "failed"
    if pct < float(thresholds["needs_practice_below"]):
        return "needs practice"
    return "solid"


def render_text(class_pct: dict, per_student: dict, thresholds: dict, order: list) -> str:
    lines = ["ATLAS topic report", "", "Class mastery:"]
    for topic in order:
        pct = class_pct[topic]
        lines.append(f"- {topic}: {pct:.1f}% ({label_for(pct, thresholds)})")
    lines.append("")
    lines.append("Weakest topics (consider more questions next time):")
    for i, topic in enumerate(order, 1):
        lines.append(f"{i}. {topic} ({class_pct[topic]:.1f}%)")
    lines.append("")
    lines.append("Per student:")
    for sid in sorted(per_student):
        parts = ", ".join(f"{t}: {per_student[sid][t]:.1f}%" for t in order)
        lines.append(f"- {sid}: {parts}")
    return "\n".join(lines) + "\n"
```

```python
# atlas/cli.py
"""CLI: python -m atlas.cli data/example1 [--thresholds path]."""
import argparse
import pathlib

from .analytics import class_mastery, student_mastery, weakest_topics
from .loader import load_questions, load_scores, load_thresholds
from .report import render_text


def main() -> None:
    parser = argparse.ArgumentParser(description="ATLAS Slice-1 topic report")
    parser.add_argument("data_dir", help="folder with questions.csv, scores.csv")
    parser.add_argument("--thresholds", default=None, help="path to thresholds.json")
    args = parser.parse_args()
    base = pathlib.Path(args.data_dir)
    questions = load_questions(str(base / "questions.csv"))
    _, scores = load_scores(str(base / "scores.csv"))
    th_path = args.thresholds or str(base / "thresholds.json")
    thresholds = load_thresholds(th_path)
    class_pct = class_mastery(questions, scores)
    per_student = student_mastery(questions, scores)
    order = weakest_topics(class_pct)
    print(render_text(class_pct, per_student, thresholds, order), end="")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m unittest tests.test_report -v`
Expected: PASS (2 tests, OK). Then smoke: `python -m atlas.cli data/example1`
Expected stdout contains "Class mastery:", "Equations: 70.0%", "Fractions: 73.3%".

- [ ] **Step 5: Commit**

```bash
git add atlas/report.py atlas/cli.py tests/test_report.py
git commit -m "feat: add CLI text report with thresholds"
```

## Self-Review

- Spec coverage: record assessments/questions/topics/points (Task 1 CSVs); class + per-student mastery + change-over-time — change-over-time deferred to Slice-1b (needs 2nd assessment folder, same math reused); simple weakest recommendation (Task 3); accept existing sheets via wide CSV (Task 1); teacher thresholds (Tasks 1+3); privacy local-only aliases (Global). Groq reasoning explicitly deferred to Slice-2 per user answer.
- Placeholder scan: no TBD/TODO; all code complete; edge handling minimal but explicit (possible==0 -> 0.0).
- Type consistency: `questions` dict shape identical across loader/analytics; `thresholds` keys identical across loader/report/cli; `order` is sorted topic list throughout.

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-09-21-atlas-slice1.md`. Two execution options:

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**
