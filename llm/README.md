llm/

This folder contains modules responsible for generating language-model-based reasoning signals.

llm_signal_engine.py:
Generates sentiment signals from financial news and textual information using a large language model.

macro_signal_engine.py:
Produces macro-level contextual signals reflecting broader economic conditions.

llm_parser.py:
Processes textual outputs from the language model into structured sentiment scores.

signal_verifier.py:
Applies consistency checks to improve robustness and reliability of language-model-generated signals.

prompt_templates.py:
Defines structured prompts used to guide the reasoning behaviour of the language model.

These modules enable the agent to incorporate qualitative reasoning alongside quantitative indicators.
