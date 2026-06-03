# Learning Roadmap: Build a Mature Personal Learning Agent from Scratch

Build it in projects. Each project builds directly on the last.

**Projects 1–3 are the MVP.**

I've noted in the capstone how each maps to your 10 architecture requirements.

---

# Project 1 — Single Good Answer (The Generator)

## Goal

Call an LLM from Python and reliably get answers in your preferred style.

## Core Concepts

* API calls
* System prompts
* Few-shot examples
* Structured output

## Stack

* Python
* One LLM SDK

## Build

1. A CLI that takes a question.
2. A system prompt encoding your traits:

   * Intuition first
   * Concise
   * Example-driven
   * Makes connections
3. Ask for answers in a fixed format.
4. Add 1–2 example answers you love as few-shot examples.

## Good Looks Like

You ask 10 varied questions and the style is consistently what you want, without re-prompting.

---

# Project 2 — Add the Judge (The Evaluator)

## Goal

A second LLM call that scores Project 1's answer against your rubric and lists weaknesses.

## Core Concepts

* LLM-as-judge
* Rubrics / G-Eval
* Separating generation from evaluation

## Stack

* DeepEval (or a hand-written judge prompt returning JSON)

## Build

1. Write the weighted rubric.
2. Judge call returns:

```json
{
  "scores": {},
  "weaknesses": [],
  "missing": [],
  "cut_these": [],
  "overall": 0
}
```

3. Print the answer and its scorecard.

## Good Looks Like

The weaknesses the judge lists are ones you'd agree with on most answers.

---

# Project 3 — Close the Loop (Iterative Refinement) ← MVP Complete

## Goal

Automatically revise until the answer passes, then present it.

## Core Concepts

* Reflection/refine loop
* Stopping conditions
* Iteration budget

## Stack

* Plain Python loop
* Later: LangGraph

## Build

```python
while score < threshold and tries < max_tries:
    regenerate(
        weaknesses_from_judge
    )
```

1. Regenerate while the score is below threshold.
2. Pass the judge's weaknesses back as instructions.
3. Make `threshold` and `max_tries` configurable.
4. Stop and present the best version.

## Good Looks Like

* Final answers are measurably better than first drafts.
* The loop always terminates.
* You can tune how picky it is.

## Worked Example

**Question:** Explain transformers.

### Draft 1

Dives directly into matrix math.

### Judge Feedback

* No intuition first.
* No example.

### Draft 2

Starts with:

> Every word can look at every other word when deciding what it means.

Adds a simple sentence example.

### Result

Judge passes. User sees Draft 2.

---

# Project 4 — Give It Memory

## Goal

Remember your goals, preferences, and past corrections across sessions.

## Core Concepts

* Persistent memory
* Semantic memory
* Episodic memory
* Context injection

## Stack

* Mem0
* Or SQLite + embeddings

## Build

1. Save standing preferences and goals.
2. Save each interaction after every session.
3. Retrieve relevant memories on new questions.
4. Inject memories into generator and judge prompts.

## Good Looks Like

It starts a new session already knowing your goals and reuses past corrections when relevant.

---

# Project 5 — Human-in-the-Loop + Real Dataset

## Goal

Create a simple interface where you rate, edit, and continuously collect training data.

## Core Concepts

* Human-in-the-loop (HITL)
* Preference-data collection
* Retrieval over your own feedback

## Stack

* Streamlit
* Chroma or SQLite-vec

## Build

1. UI showing:

   * Answer
   * Scorecard
   * Accept button
   * Edit button
   * Rate button
   * A/B comparison button
2. Save the complete interaction record.
3. Before generating:

   * Retrieve similar past corrections.
   * Feed them into generation.

## Good Looks Like

You build a clean and growing dataset, and familiar topics arrive already shaped by your history.

---

# Project 6 — Make the Judge Learn You (Optimization)

## Goal

Automatically rewrite generator and judge prompts to match your collected feedback.

No GPUs. No fine-tuning.

## Core Concepts

* Programmatic prompt optimization
* Prompts as learnable parameters
* Optimization from textual feedback

## Stack

* DSPy
* GEPA

## Build

1. Express generator and judge as DSPy modules.
2. Define:

```text
Metric = Agreement with your ratings and edits
```

3. Run GEPA over your logged dataset.
4. Compare:

   * Optimized judge
   * Hand-written judge

## Good Looks Like

The optimized judge predicts your verdicts noticeably better on unseen answers.

---

# Project 7 — Fine-Tune (Advanced / Optional)

## Goal

Bake your style into a small model so it requires less prompting, or train a dedicated evaluator.

## Core Concepts

* Preference fine-tuning (DPO)
* LoRA
* Cost/benefit analysis

## Stack

* Provider fine-tuning API
* Or Unsloth + small open-source model

## Build

1. Convert A/B selections into DPO pairs.
2. Fine-tune the model.
3. Evaluate against:

   * Held-out test set
   * Project 6 prompt-optimized version

## Good Looks Like

A model that naturally defaults to your style with a shorter prompt, and you can clearly determine whether it outperformed Project 6 enough to justify the additional complexity.

---

# Summary

| Project | Name                | Outcome                                         |
| ------- | ------------------- | ----------------------------------------------- |
| 1       | Generator           | Produce answers in your preferred style         |
| 2       | Evaluator           | Judge answer quality using a rubric             |
| 3       | Refinement Loop     | Automatically improve answers until they pass   |
| 4       | Memory              | Remember preferences, goals, and history        |
| 5       | Human-in-the-Loop   | Collect feedback and build a dataset            |
| 6       | Prompt Optimization | Learn your preferences through prompt evolution |
| 7       | Fine-Tuning         | Encode your style directly into a model         |


# Technologies Map

## LLM Fundamentals

**Learn first: ~1–2 weeks**

### How an LLM API Call Works

Learn:

* Messages
* Roles

  * `system`
  * `user`
  * `assistant`
* `temperature`
* `max_tokens`

This is the whole foundation.

Everything else is orchestration around it.

### Prompt Engineering

Learn:

* System prompts
* Few-shot examples
* Structured output

  * Asking for JSON
  * Parsing JSON

### Context Windows

Understand why you cannot just “remember everything.”

This constraint drives the entire memory design.

### Token Cost Awareness

You have already explored this with output-token minimization.

The same instinct applies here.

---

# Orchestration / Agent Frameworks

This is the glue.

## Start With No Framework

Use only:

* Raw Anthropic Python SDK
* Or raw OpenAI Python SDK

Build the loop yourself first.

You will understand agents far better after building one with plain `while` loops.

## Then Use LangGraph

Use LangGraph when you need:

* Real loops
* Branching
* State

LangGraph models your cycle exactly:

```text
generate → evaluate → improve → check stopping condition
```

This is the single most relevant framework for your goal.

## Optional Later: Pydantic AI

Use Pydantic AI later if you want lighter, more typed agents.

---

# Evaluation Systems

This is your hard 20%.

## LLM-as-Judge

Use one LLM call to score another LLM's output against criteria.

This is how your personalized evaluator starts life.

## Rubric Design

Turn vague preferences into concrete, scorable criteria.

Example:

```text
"Concise but complete"
```

Becomes:

```text
- Removes unnecessary detail
- Keeps all essential reasoning
- Uses examples only when helpful
- Does not over-explain obvious points
```

## Eval Frameworks

Use:

* `promptfoo`

  * Easy
  * Config-driven
* `DeepEval`

  * More systematic testing

---

# Memory & Retrieval

## Structured Memory

Use a plain SQLite or JSON store for:

* Goals
* Preferences
* Past feedback

This is underrated.

Start here, not with vectors.

## RAG

Retrieval-Augmented Generation means:

* Embeddings
* Vector database
* Pulling relevant past answers and feedback into context

Good local option:

* Chroma

Later options:

* Qdrant
* pgvector

## When Not to Use RAG

Do not use RAG if your data fits in the context window.

In that case, RAG adds complexity for nothing.

---

# Personalization at the Deep End

## Preference Data Collection

Collect:

* Ratings
* Edits
* Pairwise comparisons

Example:

```text
A vs B — which is better?
```

## Fine-Tuning vs Alternatives

Fine-tuning is covered honestly in the capstone section.

For a beginner, it is usually the wrong first move.

---

# Supporting Tooling

Do not skip this.

## Python Basics

Learn:

* Python fundamentals
* `venv`
* Environment variables for API keys

## Git/GitHub

Use Git/GitHub for versioning.

## Observability

Start with:

* Logging

Later graduate to:

* LangSmith
* Langfuse

These trace every step of an agent run and are invaluable for debugging loops.

---

# What Is Deliberately Not Here

Do not focus on:

* Training your own model from scratch
* Kubernetes
* Heavy MLOps
* RLHF infrastructure

None of these are essential for what you are building.

Chasing them is the most common way beginners stall.



# Final Capstone: The Personalized Iterative Learning Agent

This integrates Projects 1–7 into the system you described, then addresses the deep-end question honestly.

---

# Architecture

## Mapping Directly to Your 10 Requirements

A LangGraph agent with this state and flow:

## 1. Generate

Produce an initial answer, conditioned on:

* Memory

  * Your goals
  * Your preferences
* RAG-retrieved past feedback

## 2. Evaluate

The personalized evaluator scores against criteria assembled from:

* Stored preferences
* Retrieved corrections

**Maps to requirements:** 2, 7

## 3. Diagnose

The evaluator outputs specific weaknesses:

* Missing context
* Unclear sections
* Unnecessary detail

**Maps to requirement:** 3

## 4. Improve

Rewrite the answer by addressing the diagnosis.

**Maps to requirement:** 4

## 5. Stopping Check

Conditional edge exits on:

* Score threshold
* Max iterations
* Convergence / no improvement

**Maps to requirement:** 9

## 6. Present + Capture Feedback

Show the answer, then capture:

* Your rating
* Your edits
* Your notes

**Maps to requirement:** 5

## 7. Persist

Write feedback to:

* Structured store
* Vector store

**Maps to requirements:** 6, 10

## 8. Track

Log scores per run for a quality-over-time view.

**Maps to requirement:** 8

---

# Memory Design

Memory has two tiers.

## 1. Long-Term Structured Memory

Stored in SQLite:

* Identity
* Learning goals
* Explicit preferences
* Full feedback history

## 2. Retrieval Layer

Stored in Chroma:

* Embedded past answers
* Embedded corrections
* Similarity recall

## 3. Session State

Stored in LangGraph:

* Current answer
* Score
* Iteration count

---

# The Personalized-Evaluator Question

Read this carefully.

Your stated end goal is:

> A digital representation of my preferences that automatically judges answers before presenting them.

There are three ways to build that judge, in increasing cost and decreasing advisability for you right now.

---

## Option 1 — Prompt + RAG Evaluator

**Recommended, and where you should stay for a long time.**

The judge is an LLM whose rubric is dynamically built from your stored preferences and retrieved feedback.

It improves the instant you add feedback:

* No training
* No waiting
* No retraining loop

For a one-person system, this approximates your preferences remarkably well and is what Projects 6–7 build.

---

## Option 2 — Few-Shot “Preference Exemplar” Evaluator

Curate your best correction pairs and feed them as examples to the judge.

This is:

* Cheap
* Effective
* A natural extension of Option 1

---

## Option 3 — Fine-Tuned Evaluator Model

**The deep end — likely unnecessary.**

Fine-tuning a model to mimic your judgments needs:

* Hundreds to thousands of high-quality preference examples
* Money per training run
* Retraining as your taste evolves
* Careful evaluation to avoid doing it badly

For a single user's preferences, Options 1–2 usually match or exceed it at a fraction of the effort.

Do not fine-tune until you've hit a concrete, measured wall that prompting + RAG provably cannot clear.

You will only know that because Project 7's tracking shows quality stalling despite plenty of feedback data.

If you reach that point, you will already have:

* The dataset from Project 5
* The judgment to do it properly

That is the right time, not now.

---

# Preference Data Collection Methods

In order of value-per-effort:

## 1. Explicit Ratings

The easiest signal to collect.

## 2. Your Edits to Answers

The richest signal.

The diff is the lesson.

## 3. Pairwise Comparisons

Example:

> Which of these two is better?

This is the gold standard for training a judge if you ever go that route.

## 4. Free-Text Notes

Great for the prompted evaluator, because you can feed them in verbatim.

---

# Implementation Roadmap

## MVP: Projects 1–3

A CLI that iteratively self-improves with stopping conditions.

Usable in a weekend or two.

---

## Personalized Core: Projects 4–7

This includes:

* Memory
* Feedback
* RAG
* Personalized evaluator

This is the real product and where most learning happens.

---

## Production Polish

Only if you want it.

Possible additions:

* Web UI

  * Streamlit is the gentle on-ramp
* LangSmith / Langfuse tracing
* Structured learning-path generation
* Quality dashboard

None of these changes the core.

They make the core pleasant to live in.

---

# Closing Advice

Your instinct to specify the whole advanced system upfront is good engineering thinking.

But the highest-leverage move here is the opposite:

> Build Project 2 this week.

The self-critique loop is the heart of the entire design.

It takes about 50 lines, and actually watching an answer improve itself will teach you more about what your evaluator needs than any amount of architecture planning.

The rest of the roadmap will make far more sense once you've felt that loop work.

---

# Next Step

Write the actual code for Project 1 and Project 2 so you have a running self-improving agent today.

That is the fastest way to make all of this concrete.
