from typing import List, Dict, Any

class DialogueFormatter:
    def __init__(self, character_name: str, initial_state: str):
        self.character_name = character_name
        self.initial_state = initial_state

    # 環境情報を文字列にフォーマット
    def format_environments(self, environments: Dict[str, str]) -> str:
        return "\n".join([f"{desc} [{env_id}]" for env_id, desc in environments.items()])

    # 細菌のストーリーをフォーマット
    def format_recent_story(self, dialogue_history: List[Dict], limit: int = 1) -> str:
        recent = [entry for entry in dialogue_history[-limit:] 
                if entry['type'] in ['initial_state', 'user_action', 'world_simulation']]
        if recent:
            return recent[-1]['content']
        return self.initial_state

    # 対話履歴をフォーマット
    def format_dialogue_history(self, dialogue_history: List[Dict], limit: int = 3) -> str:
        recent = dialogue_history[-limit:] if dialogue_history else []
        formatted = []
        
        for entry in recent:
            if entry['type'] == 'user_action':
                formatted.append(f"ユーザー: {entry['content']['action_content']}")
            elif entry['type'] == 'world_simulation':
                if entry['content']['story_progress']:
                    formatted.append(f"{self.character_name}: {entry['content']['story_progress']}")
                if entry['content']['response']:
                    formatted.append(f"{self.character_name}: {entry['content']['response']}")
                if entry['content']['action_need']:
                    formatted.append(f"状況: {entry['content']['action_need']}")
        
        return "\n".join(formatted) if formatted else "対話履歴なし"