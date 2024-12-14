from typing import Tuple, Dict, Any
import re
from utils import GPTClient

class UserSimulator:
    def __init__(self, gpt_client: GPTClient):
        self.gpt_client = gpt_client

    def simulate(self, user_input, environments, recent_story, character_status, dialogue_history, current_environment):
        prompt_instruction = self._create_instruction_prompt(user_input)
        prompt_input = self._create_input_prompt(
            environments,
            recent_story,
            character_status,
            dialogue_history
        )
        
        response = self.gpt_client.Ans_GPT(prompt_instruction, prompt_input)
        return self._parse_response(response, current_environment)

    # user_simulation用プロンプトを生成(instruction)
    def _create_instruction_prompt(self, user_input):
        return f"""
        あなたはストーリーの中のキャラクターと対話するエージェントです。キャラクターの詳細を提供し、ストーリーとキャラクターの状態に基づいてキャラクターと対話する必要があります。
        ユーザーから以下の入力を受け取りました：
        {user_input}

        このユーザー入力を、以下の4つのタイプのいずれかに変換してください：

        1. Continue Generation（ストーリーを続ける）
        - 単に"continue generation"と出力
        2. Describe Character Details and Continue Generation（キャラクターの詳細を追加してストーリーを続ける）
        - キャラクターの性格や特徴についての追加情報を提供
        3. Interact with Character（キャラクターとの対話）
        - キャラクターと遊ぶ、餌をやる、休ませる、清潔にするなどの具体的なアクション
        - 一度に1つの状態のみを更新するアクションを選択
        4. Move the Character to New Environments（新しい環境への移動）
        - 利用可能な環境の中から新しい場所を選択
        
        応答を選択する際の優先順位：
        1. ユーザーの入力内容を最優先で考慮してください。入力した内容から異なる行動はしないでください。
        2. キャラクターの現在の状態（空腹度、エネルギー、楽しさ、衛生状態）を考慮してください
        3. 状態が危険な場合（エネルギー、楽しさ、衛生状態が30%以下、または空腹度が70%以上）は、その状態に応じた行動や発言を含めてください

        出力は70語未満の簡潔な行動指示のみとしてください。ストーリーは生成しないでください。
        キャラクターの状態には4種類あります：空腹度、エネルギー、楽しさ、衛生状態。状態はエネルギー、楽しさ、衛生状態が100%、空腹度が0%が最も良い状態です。
        対話は与えられた環境と以前に生成されたストーリーに基づいて合理的であるべきです。

        以下は出力の例です：
        出力例1：
        [Continue Generation]

        出力例2：
        [Describe Character Details and Continue Generation]
        私の猫は活発で、水遊びが大好きです。

        出力例3：
        [Interact with Character]
        私は猫を撫でて、「いい子だね」と言います。

        出力例4：
        [Interact with Character]
        私は猫に餌をあげます。

        出力例5：
        [Move the Character to New Environments]
        私は猫を暖炉の前に連れて行きます。[ENVN]
        """

    # user_simulation用プロンプトを生成(input)
    def _create_input_prompt(self, environments, recent_story, character_status, dialogue_history):
        return f"""
        [Environment]
        {environments}

        [Initial State]
        {recent_story}

        [Character Status]
        空腹度：{character_status['hunger']}%
        エネルギー：{character_status['energy']}%
        楽しさ：{character_status['fun']}%
        衛生状態：{character_status['cleanliness']}%

        [Dialogue History]
        {dialogue_history}
        """

    # GPTの応答を解析してアクションタイプと内容を抽出
    def _parse_response(self, response, current_environment):
        response = response.strip()
        
        if '[Continue Generation]' in response:
            return 'continue_generation', 'continue generation'
        
        elif '[Describe Character Details and Continue Generation]' in response:
            content = response.replace('[Describe Character Details and Continue Generation]', '').strip()
            return 'describe_details', content
        
        elif '[Interact with Character]' in response:
            content = response.replace('[Interact with Character]', '').strip()
            return 'interact', content
        
        elif '[Move the Character to New Environments]' in response:
            content = response.replace('[Move the Character to New Environments]', '').strip()
            # ENV番号を抽出
            env_match = re.search(r'\[ENV(\d+)\]', content)
            if env_match:
                content = re.sub(r'\[ENV\d+\]', '', content).strip()
            return 'move', content
        
        else:
            # デフォルトはContinue Generationとして扱う
            return 'continue_generation', 'continue generation'