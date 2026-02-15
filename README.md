# Karachi Street Narrator

**A Multi-Agent Narrative System for Hackfest x Datathon 2026**

*Team Hakuna Matata: Ali ur Rehman, Hamza Ali*

---

## Overview

An autonomous narrative engine that transforms a seed story into a coherent 25-turn narrative. Characters interact with distinct personas, maintain memory of past interactions, and execute physical actions that change the story state. A Director orchestrates the flow while a reasoning layer decides between dialogue and action.

**Key Innovation:** Director narrates in English while characters speak in Roman Urdu, reflecting Karachi's multicultural street culture.

---

## Quick Start

**Prerequisites:** Python 3.11+ and `uv` package manager

```bash
# Clone and setup
git clone https://github.com/YOUR_USERNAME/GenAi_DSS.git
cd GenAi_DSS
uv sync

# Configure API key
echo "GOOGLE_API_KEY=your_api_key_here" > .env

# Run simulation
uv run src/main.py
```

The system loads the rickshaw accident seed story, initializes agents, runs 25 dialogue turns, and saves outputs to `story_output.json` and `prompts_log.json`.

---

## Architecture

![State Diagram](State%20Diagram%20V2.svg)

```
Narrative Loop: Director → Character → State Update → Check Conclusion → Repeat
```

**Director Agent:** Orchestrates turn-taking, selects next speaker, monitors story objectives, and decides when actions are needed.

**Character Agents:** Embody distinct personas, speak in Roman Urdu street slang, consult vector-based memory, and must include physical actions in every response.

**Story State Manager:** Centralized hub tracking dialogue history, turn count, character inventories, environmental variables, and story metadata.

**Reasoning Layer:** Mediates between dialogue and action based on context, memory retrieval, and story pacing to prevent loops and maintain momentum.

---

## Action System

Characters express physical presence through bracketed actions `[ACTION: ...]` that modify story state.

**Five Mandatory Categories:**

| Category | Examples |
|----------|----------|
| Movement | pacing, stepping, leaning |
| Expression | glaring, sweating, smirking |
| Interaction | pointing, touching, gesturing |
| Sensory | hearing horns, feeling heat |
| Conflict | blocking, reaching, pushing |

Every character response must include at least one action to ensure embodied storytelling and prevent pure dialogue loops.

---

## Memory & Reasoning

**Vector-Lite Memory:** Characters maintain individual memory stores. Before speaking, the system retrieves relevant past interactions using vector-based retrieval and injects them into the prompt context.

```python
self.character_memories = {char["name"]: [] for char in characters}
```

**Reasoning Layer:** Decides between dialogue and action by analyzing current state, memory context, and story pacing. Increases action probability when conflict stalls to maintain momentum.

---

## Output Files

**`story_output.json`** - Complete narrative trace
```
├─ Metadata: title, seed description
├─ Events: chronological list with type, speaker, content, turn
└─ Conclusion: resolution reason
```

**`prompts_log.json`** - Full audit trail
```
├─ timestamp: request time
├─ agent: Director or Character name
├─ prompt: exact text sent to LLM
└─ response: raw model output
```

---

## Technical Solutions

| Challenge | Solution |
|-----------|----------|
| Turn Limit Management | Centralized turn counter with iteration checks |
| Character Voice Consistency | Prompt engineering for Roman Urdu and street slang |
| Loop Prevention | Reasoning layer monitors repetition and triggers actions |
| JSON Reliability | Rigorous validation before file writes |
| Network Stability | Local prompt logging with checkpoint recovery |

---

## Key Features

```
✓ Director-Actor Architecture        ✓ Physical Action System (5 categories)
✓ Bilingual Design (EN/Roman Urdu)   ✓ Turn-Limited Execution (25 max)
✓ Vector-Lite Memory System          ✓ Complete Prompt Logging
✓ Intelligent Reasoning Layer        ✓ State-Changing Actions
```

---

## Conclusion

Karachi Street Narrator demonstrates how structured multi-agent systems can generate rich, culturally authentic narratives within tight constraints. By combining a Director for orchestration, vector-based character memory, mandatory physical actions, and intelligent reasoning between dialogue and state changes, we achieve autonomous storytelling that is coherent, embodied, and true to Karachi's street culture.

The architecture emphasizes separation of concerns: the Director orchestrates, characters inhabit their roles, and the state manager maintains coherence across 25 turns of dynamic narrative generation.