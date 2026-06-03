I am going to build a matured personal learning agent from sratch.

Learning roadmap — build it in projects
Each project builds directly on the last. Projects 1–3 are your MVP. I've noted in the capstone how each maps to your 10 architecture requirements.
Project 1 — Single good answer (the Generator)

Goal: Call an LLM from Python and reliably get answers in your preferred style.
Core concepts: API calls, system prompts, few-shot examples, structured output.
Stack: Python + one LLM SDK.
Build: (a) A CLI that takes a question. (b) A system prompt encoding your traits (intuition first, concise, example, connections). (c) Ask for the answer in a fixed format. (d) Add 1–2 example answers you love as few-shot.
Good looks like: You ask 10 varied questions and the style is consistently what you want, without re-prompting.

Project 2 — Add the judge (the Evaluator)

Goal: A second LLM call that scores Project 1's answer against your rubric and lists weaknesses.
Core concepts: LLM-as-judge, rubrics/G-Eval, separating generation from evaluation.
Stack: + DeepEval (or a hand-written judge prompt returning JSON).
Build: (a) Write the weighted rubric. (b) Judge call returns {scores, weaknesses, missing, cut_these, overall}. (c) Print the answer and its scorecard.
Good looks like: The weaknesses the judge lists are ones you'd agree with on most answers.

Project 3 — Close the loop (Iterative refinement) ← MVP complete

Goal: Automatically revise until the answer passes, then present.
Core concepts: the reflection/refine loop, stopping conditions, iteration budget.
Stack: plain Python loop (later: LangGraph).
Build: (a) while score < threshold and tries < max_tries: regenerate, passing the judge's weaknesses back in as instructions. (b) Make threshold and max_tries config values. (c) Stop and present the best version.
Good looks like: Final answers are measurably better than first drafts; the loop always terminates; you can tune how picky it is.

Worked example: you ask "explain transformers." Draft 1 dives into matrix math → judge flags "no intuition first, no example" → draft 2 opens with the "every word looks at every other word" intuition and adds a sentence example → judge passes → you see draft 2.
Project 4 — Give it memory

Goal: Remember your goals, preferences, and past corrections across sessions.
Core concepts: persistent memory, semantic vs episodic store, context injection.
Stack: + Mem0 (or SQLite + embeddings).
Build: (a) Save your standing preferences and goals. (b) After each session, save the interaction. (c) On each new question, fetch relevant memories and inject them into the generator and judge prompts.
Good looks like: It greets a new session already knowing your goals, and visibly reuses a past correction on a related topic.

Project 5 — Human-in-the-loop + a real dataset

Goal: A simple interface where you rate/edit, and every interaction is logged.
Core concepts: HITL, preference-data collection, RAG over your own feedback.
Stack: + Streamlit + Chroma/SQLite-vec.
Build: (a) UI showing the answer + scorecard with buttons: accept, edit, rate, A/B. (b) Save the full record (see "preference data" above). (c) Add retrieval: before generating, pull your most similar past corrections and feed them in.
Good looks like: You have a clean, growing dataset, and answers on familiar topics now arrive pre-shaped by your history.

Project 6 — Make the judge learn you (optimization)

Goal: Automatically rewrite the generator and judge prompts to match your collected feedback — no GPUs, no fine-tuning.
Core concepts: programmatic prompt optimization, prompts as learnable parameters, optimizing from textual feedback.
Stack: + DSPy / GEPA.
Build: (a) Express your generator and judge as DSPy modules. (b) Define the metric = agreement with your ratings/edits. (c) Run GEPA over your logged data to evolve better prompts. (d) Compare the optimized judge's agreement vs your hand-written one.
Good looks like: The optimized judge predicts your verdicts noticeably better, measured on answers it hasn't seen.

Project 7 — Fine-tune (advanced / optional)

Goal: Bake your style into a small model so it needs less prompting, or train a dedicated evaluator.
Core concepts: preference fine-tuning (DPO), LoRA, honest cost/benefit.
Stack: a provider fine-tuning API, or Unsloth + a small open model.
Build: (a) Convert your A/B picks into DPO pairs. (b) Fine-tune. (c) Evaluate against your held-out test set and against the Project 6 prompt-optimized version.
Good looks like: A model that defaults to your style with a shorter prompt — and you can clearly state whether it beat Project 6 enough to justify the effort.