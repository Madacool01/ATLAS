# Context — Project "ATLAS" (working name)

> Living document. Everything we know and want, in plain language. No code, no technical decisions here — just the idea, the goals, and the plan. Update this file whenever the vision changes.

---

## Where the idea came from

I talked with my math teacher (who also teaches computer science) about using agentic AI and machine learning to solve real problems. This project came out of that conversation. He liked the idea and asked me to start building a first prototype.

## The problem today

Our teacher gives roughly five exams per semester, or two exams plus two or three quizzes. For every one of them he:

1. Types out the questions and notes which topic(s) each question covers.
2. When results are out, records each student's points.
3. Looks at the results to see which topics students struggle with.
4. Decides which areas need more practice, and can add a few more questions on those weak topics in the next exam to make sure students really understood.

All of that is manual work in spreadsheets, and the insight (which topics are weak, what to do next) lives only in his head.

## The core idea

A tool that does steps 1–4 for him:

- He enters each assessment (exam or quiz) with its questions and their topics, plus the points each student earned per question.
- The tool shows which topics the class struggles with — and which topics each individual student struggles with.
- It then recommends what to do next: which topics need more questions or practice on the next exam/worksheet, and why.
- Over the semester it can show whether the recommendation worked: if a topic was weak and he practiced it, did the score on that topic go up on the next assessment?

The smallest unit of everything is the **question tied to a topic**. Every insight is built from that.

## What the first version should do

- Let the teacher record assessments, questions, topics, and per-student points without pain.
- Show per-topic mastery for the whole class and per student, and how it changes from assessment to assessment.
- Produce a simple recommendation: "these are the weakest topics, consider adding more questions on them next time."
- Work with what the teacher already has — ideally it should accept the data the way he currently keeps it (e.g., his existing sheets), instead of forcing him to re-type everything differently.

## The AI part (already decided)

- **No machine learning in the first version.** We don't need it yet.
- Instead, we use a **Groq Cloud model** (generous free tier) to *reason* over the percentages: it looks at the results and decides which topics need the most questions next, and suggests concrete actions for the next worksheet — based on its reasoning, not hard-coded rules.
- The teacher stays in the loop: the AI suggests, the teacher decides.

## Teacher stays in control

- Teachers can **define what each percentage means** themselves — for example which range counts as "failed," which as "needs practice," which as "solid." The tool uses *their* definitions, not ours, when flagging topics and phrasing recommendations.

## Ideas for later (v2+)

- **Scan an exam photo:** pay for API calls so a picture of an exam is automatically read and each exercise is tagged with the topics it covers (e.g., "Exercise 1 covers topics X, Y, Z"), eliminating the manual typing. The teacher would only confirm or correct the suggestions.
- More agentic features: the AI reads the analytics and drafts the next exam blueprint or generates practice questions for weak topics, teacher approves.

## What success looks like

- The teacher actually uses it for one real (anonymized) assessment and finds it easier than his spreadsheet.
- The tool correctly names the topics the class struggles with.
- It proves its own value: after practicing a weak topic, the score on that topic improves on the next assessment.

## Privacy rules (non-negotiable)

- Student scores stay local. Students are referenced by alias/ID, never by name in anything that leaves the machine.
- Only question text (no names, no scores) should ever be sent to an external AI service.

## Name

We want a strong "scientific instrument" style name (like PERSEUS, TESSERACT, RUNE). Candidates so far — favorite first:

1. **ATLAS** — Assessment & Topic Learning Analytics System (current favorite; also an atlas = map of the class's knowledge)
2. **EUCLID** — Evaluating Understanding of Curricula & Learning through Item Diagnostics (nice nod for a math teacher)
3. **PRISM** — Performance Reporting & Item-Subtopic Mapping
4. **AXIOM** — Analytics eXam Intelligence & Outcome Mapping
5. **QUARK** — Question-level Understanding Analytics & Reporting Kit
6. **DELTA** — Diagnostic Evaluation of Learning & Topic Analytics

Final name still to be confirmed (ideally with the teacher).

## Open questions

- Exactly how does the teacher record results today? (Shadow him once and copy his workflow.)
- Does he care more about the class-wide view or individual students first?
- Which topics list does he use — does he already have a fixed list of topic names?
- How does he want to receive the recommendation — on screen, printable page, or short summary?

## Next steps

1. Confirm the name and the workflow details with the teacher.
2. Build the first version: record data → see topic strengths/weaknesses → Groq-powered recommendations → teacher-defined percentage meanings.
3. Test it with one real anonymized assessment and iterate on his feedback.
