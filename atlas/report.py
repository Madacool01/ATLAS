"""text report using teacher defined thresholds."""  # yeah just saying what this file is about


def label_for(pct: float, thresholds: dict) -> str:  # hey this one turns a percent into a teacher label
    if pct < float(thresholds["failed_below"]):  # below the failed line, like under fifty
        return "failed"  # yep failed zone
    if pct < float(thresholds["needs_practice_below"]):  # below the solid line, like under seventy five
        return "needs practice"  # middle zone, needs more reps
    return "solid"  # above it all, solid zone


def render_text(class_pct: dict, per_student: dict, thresholds: dict, order: list) -> str:  # hey this one builds the whole text report
    lines = ["ATLAS topic report", "", "Class mastery:"]  # start with a title plus class section header
    for topic in order:  # walk topics worst first, like equations then fractions
        pct = class_pct[topic]  # grab the class percent for this topic
        lines.append(f"- {topic}: {pct:.1f}% ({label_for(pct, thresholds)})")  # one line like equations seventy with label
    lines.append("")  # blank line to breathe
    lines.append("Weakest topics (consider more questions next time):")  # header for the recommendation bit
    for i, topic in enumerate(order, 1):  # number them starting at one
        lines.append(f"{i}. {topic} ({class_pct[topic]:.1f}%)")  # one line per topic with its percent
    lines.append("")  # another blank line
    lines.append("Per student:")  # header for the kid by kid part
    for sid in sorted(per_student):  # go kid by kid in order, like s01 then s02
        parts = ", ".join(f"{t}: {per_student[sid][t]:.1f}%" for t in order)  # join their topics like fractions seventy
        lines.append(f"- {sid}: {parts}")  # one line per kid
    return "\n".join(lines) + "\n"  # glue it all with newlines plus a final one
