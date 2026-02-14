import asyncio
import json
import sys
import os
from pathlib import Path

current_dir = Path(__file__).parent
project_root = current_dir.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.config import StoryConfig
from src.agents.character_agent import CharacterAgent
from src.agents.director_agent import DirectorAgent
from src.graph.narrative_graph import NarrativeGraph
from src.story_state import StoryStateManager


async def main():
    # Load seed story from examples
    examples_dir = project_root / "examples" / "rickshaw_accident"

    seed_story = json.loads((examples_dir / "seed_story.json").read_text())

    # Load character configs
    char_configs = json.loads((examples_dir / "character_configs.json").read_text())

    # Initialize config
    config = StoryConfig()

    # Create character agents
    characters = [
        CharacterAgent(char["name"], config)
        for char in char_configs
    ]
    # Create director
    director = DirectorAgent(config)

    # Initialize StoryStateManager
    story_manager = StoryStateManager(seed_story, char_configs, config)

    # Build and run narrative graph
    story_graph = NarrativeGraph(config, characters, director)

    print("Starting Narrative Game...")
    print(f"Title: {seed_story['title']}")
    print(f"Scenario: {seed_story['description']}\n")

    # Run the game
    final_state = await story_graph.run(
        seed_story=seed_story,
        character_profiles=story_manager.state.character_profiles
    )

    # Print results
    print("\n=== STORY TRANSCRIPT ===\n")
    dialogue_history = final_state.get("dialogue_history", [])
    for turn in dialogue_history:
        if isinstance(turn, dict):
            print(f"[Turn {turn.get('turn_number')}] {turn.get('speaker')}:")
            print(f"  {turn.get('dialogue')}\n")
        else:
            print(f"[Turn {turn.turn_number}] {turn.speaker}:")
            print(f"  {turn.dialogue}\n")

    print(f"\n=== CONCLUSION ===")
    total_turns = final_state.get("current_turn", 0)
    print(f"Ended after {total_turns} turns")
    print(f"Reason: {final_state.get('conclusion_reason')}")

    output_path = project_root / "story_output.json"

    output_data = {
        "title": seed_story.get("title"),
        "seed_story": seed_story,
        "events": final_state.get("events", []),
        "metadata": {
            "total_turns": total_turns,
            "conclusion_reason": final_state.get("conclusion_reason")
        }
    }

    # 2. Use encoding to ensure special characters (Urdu/Slang) save correctly
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, default=str)

    print(f"\nStory successfully saved to: {output_path}")

    # Save prompts log
    all_logs = []
    for log in director.logs:
        log["role"] = "Director"
        all_logs.append(log)

    for char in characters:
        for log in char.logs:
            log["role"] = f"Character ({char.name})"
            all_logs.append(log)

    all_logs.sort(key=lambda x: x.get("timestamp", 0))

    prompts_path = project_root / "prompts_log.json"
    with open(prompts_path, "w", encoding="utf-8") as f:
        json.dump(all_logs, f, indent=2, default=str)

    print(f"Prompts successfully saved to: {prompts_path}")


if __name__ == "__main__":
    asyncio.run(main())