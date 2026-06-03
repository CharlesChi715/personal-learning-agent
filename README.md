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
