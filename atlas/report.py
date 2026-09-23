def label_for(pct: float, thresholds: dict) -> str:
    if pct < float(thresholds["failed_below"]):  # below the failed line, like under fifty
        return "failed"  # failed zone
    if pct < float(thresholds["needs_practice_below"]):  # below the solid line, like under seventy five
        return "needs practice"  # needs more practice
    return "solid"  #


def render_text(class_pct: dict, per_student: dict, thresholds: dict, order: list) -> str:  # whole text report
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
