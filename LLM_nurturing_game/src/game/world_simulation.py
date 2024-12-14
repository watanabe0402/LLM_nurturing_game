from typing import Dict, Any
import re
from utils import GPTClient

class WorldSimulator:
    def __init__(self, gpt_client: GPTClient):
        self.gpt_client = gpt_client

    def simulate(self, character_name, character_type, personalities, abilities,environments, recent_story, current_environment, user_input, character_status):
        prompt_instruction = self._create_instruction_prompt(character_name)
        prompt_input = self._create_input_prompt(
            character_name=character_name,
            character_type=character_type,
            personalities=personalities,
            abilities=abilities,
            environments=environments,
            recent_story=recent_story,
            current_environment=current_environment,
            user_input=user_input,
            character_status=character_status
        )
        
        response = self.gpt_client.Ans_GPT(prompt_instruction, prompt_input)
        return self._process_response(response, character_name)

    # world_simulationのプロンプト（instruction）
    def _create_instruction_prompt(self, character_name):
        return f"""
        あなたは人間の指示によって定義されたキャラクターに対する世界として機能するエージェントです。
        まず世界の潜在的な環境を生成し、その後その世界で生活するキャラクターのストーリーを生成する必要があります。
        ストーリーはゲームのように聞こえ、ユーザーの対話のための余地を残す必要があります。
        ストーリーを生成する際は、1つずつ生成し、各ストーリーの分割は視覚的なイメージで捉えられるように単純にする必要があります。
        人間はキャラクターに関する追加情報を中断して提供することができ、あなたは与えられた情報に基づいてキャラクターの反応と後続のストーリーを生成する必要があります。

        以下は従うべき指示事項です：
        1. 新しい環境が必要な場合、"[Environment description][ENV N]"の形式で説明してください。環境の総数は7を超えないようにしてください。説明は環境に焦点を当て、環境内のキャラクターや人間、動物への言及は避けてください。
        2. 各ストーリー分割を生成する際は、必ず"[Splitted story part][ENV N]"の形式に従ってください。[ENV N]は、そのストーリーが起こる環境を示します。1回に1つのストーリー分割を生成してください。
        3. 同じ環境でストーリーを生成し、人間の指示で明示的に求められた場合にのみ、次の環境に移動してください。
        4. 各分割されたストーリーは50語を超えないようにしてください。内容は1つの視覚的イメージに含められるものにする必要があります。
        5. ストーリー分割を生成する際は、メインキャラクターに言及するときは常に、そのキャラクターの前に"sks"という単語を付けてください。常にキャラクターをその名前で参照し（例："sks {character_name}"）、"he"や"she"での参照は避けてください。
        6. メインキャラクター以外のキャラクターの前には"sks"という単語を付けないでください。
        7. 人間から与えられた新しい指示に基づいてストーリーの生成を継続してください。必要に応じて新しい環境を追加できます。
        8. できるだけ多様な環境とストーリーを生成するように努めてください。
        9. ユーザーからの対話がある場合は、[Response]セクションでキャラクターの反応を生成し、その後にストーリー分割を生成してください。
        10. キャラクターの状態には4種類あります：空腹度、エネルギー、楽しさ、衛生状態。状態はエネルギー、楽しさ、衛生状態が100%、空腹度が0%が最も良い状態です。
        11. 毎回少なくとも15%ずつ状態を更新してください。生成を継続する際は4つの状態すべてを更新し、ユーザーが指示を提供する際は部分的な状態を更新してください。
        12. 状態が危険（エネルギー、衛生状態、楽しさが0%以下、または空腹度が100%以上）な場合は、[Action Needed]を出力してください。

        以下は出力の例です：
        [Response]
        「もう疲れたよ。休憩しようかな。」

        [Splitted story part][ENV1]
        sksモモは疲れた様子で教室の机に寄りかかり、魔法の本を読もうとしますが、集中力が続きません。

        [Character State]
        空腹度: 15%
        エネルギー: 5%
        楽しさ: 35%
        衛生状態: 85%

        [Action Needed]
        モモのエネルギーが危険な水準まで低下しています。休息を取らせる必要があります。
        """

    # world_simulationのプロンプト（input）
    def _create_input_prompt(
        self, character_name, character_type, personalities, abilities, environments, recent_story, current_environment, user_input, character_status):
        return f"""
        [Character Details]
        名前：{character_name}
        種類：{character_type}
        性格：{', '.join(personalities)}
        特技：{', '.join(abilities)}

        [Environment]
        {environments}

        [Original Story]
        {recent_story}{current_environment}

        Human:[Instruction] 
        {user_input}

        [Character Status]
        空腹度：{character_status['hunger']}%
        エネルギー：{character_status['energy']}%
        楽しさ：{character_status['fun']}%
        衛生状態：{character_status['cleanliness']}%
        """

    # 応答の処理してコンテンツを抽出
    def _process_response(self, response, character_name):
        content = {
            'story_progress': None,
            'response': None,
            'action_need': None,
            'status': {
                'hunger': 0,
                'energy': 100,
                'fun': 100,
                'cleanliness': 100
            },
            'current_environment': None
        }
        
        # Character Stateの抽出と状態更新
        state_match = re.search(
            r'空腹度:\s*(\d+)%\s*エネルギー:\s*(\d+)%\s*楽しさ:\s*(\d+)%\s*衛生状態:\s*(\d+)%',
            response,
            re.DOTALL
        )   
        if state_match:
            content['status'].update({
                'hunger': int(state_match.group(1)),
                'energy': int(state_match.group(2)),
                'fun': int(state_match.group(3)),
                'cleanliness': int(state_match.group(4))
            })
        
        # ストーリーの抽出
        story_match = re.search(
            r'\[Splitted story part\]\[ENV(\d+)\](.*?)(?=\[Character State\])',
            response,
            re.DOTALL
        )
        if story_match:
            story_text = story_match.group(2).strip()
            story_text = re.sub(f'sks\s*{character_name}', character_name, story_text)
            content['story_progress'] = story_text
            content['current_environment'] = f'ENV{story_match.group(1)}'
        
        # レスポンスの抽出
        if '[Response]' in response:
            response_text = re.search(
                r'\[Response\](.*?)(?=\[Splitted story part\])',
                response,
                re.DOTALL
            )
            if response_text:
                response_text = response_text.group(1).strip()
                response_text = re.sub(f'sks\s*{character_name}', character_name, response_text)
                response_text = re.sub(
                    r'\[Character State\].*?(?=\[|$)',
                    '',
                    response_text,
                    flags=re.DOTALL
                )
                content['response'] = response_text.strip()

        # Action Neededの抽出
        if '[Action Needed]' in response:
            action_match = re.search(r'\[Action Needed\](.*?)(?=\[|$)', response, re.DOTALL)
            if action_match:
                action_text = action_match.group(1).strip()
                action_text = re.sub(f'sks\s*{character_name}', character_name, action_text)
                action_text = re.sub(
                    r'\[Character State\].*?(?=\[|$)',
                    '',
                    action_text,
                    flags=re.DOTALL
                )
                content['action_need'] = action_text.strip()

        return content