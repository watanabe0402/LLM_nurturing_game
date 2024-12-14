import re
from utils import GPTClient

class GameInitializer:
    def __init__(self, gpt_client: GPTClient):
        self.gpt_client = gpt_client

    def initialize(self, character_name, character_type, story_topic):
        init_prompt = self._create_init_prompt(character_name, character_type, story_topic)
        init_question = self._create_init_question(character_name, character_type, story_topic)
        
        response = self.gpt_client.Ans_GPT(init_prompt, init_question)
        return self._extract_information(response)

    # ゲーム初期化用のプロンプトを生成
    def _create_init_prompt(self, character_name, character_type, story_topic):
        return f"""
        あなたはキャラクターの世界をシミュレーションするエージェントです。
        {character_name}という{character_type}の{story_topic}についての初期設定を行ってください。

        以下の要素を生成してください：

        1. キャラクターの詳細設定
        [Character Details]
        - 性格（3つ程度の特徴）：
        - 特技や能力：

        2. 活動環境リスト（5つ程度）
        [Environment]
        - [ENV1] {story_topic}に関連する主要な環境の詳細な説明
        - [ENV2] ～ [ENV5] その他の関連する環境の説明
        （※環境の説明には人物やキャラクターへの言及を避け、視覚的な描写を心がけてください）

        3. 初期状態設定
        [Original Story]
        {character_name}の物語開始時の状況を簡潔に説明する文章

        生成の際の注意点：
        - {character_type}の特性を活かした設定にしてください
        - {story_topic}に沿った環境とシチュエーションを設定してください
        - すべての要素が互いに関連し、一貫性のある世界観を作成してください
        - 後続のシミュレーションで活用できる具体的な設定を含めてください


        以下は出力の例です：
        [Character Details]
        性格：
        - 好奇心旺盛で新しいことに興味津々
        - 少し臆病だが、友達のためには勇気を出せる
        - マイペースで独創的な発想の持ち主
        特技や能力：
        - 小さな浮遊魔法が使える
        - 動物たちと会話ができる
        - 不思議な予感を感じ取れる

        [Environment]
        [ENV1] 古い石造りの教室。天井まで届く本棚と、キラキラと光る魔法の粒子が漂っている
        [ENV2] 色とりどりの花が咲く中庭。噴水から虹色の水が流れ出している
        [ENV3] 星々が常に輝く天文台。望遠鏡と魔法の星図が並んでいる
        [ENV4] 小動物たちが集まる学校裏の小さな森。きのこの輪が点在している
        [ENV5] 様々な魔法道具が並ぶ実習室。壁には不思議な模様が描かれている

        [Initial State]
        魔法学校に入学したばかりのモモは、新しい環境に少し緊張しながらも、これから始まる不思議な学校生活に胸を躍らせている。初めて訪れた教室で、キラキラと漂う魔法の粒子に魅了されている。
        """

    # 初期化用の質問を生成
    def _create_init_question(self, character_name, character_type, story_topic):
        return f"""
        キャラクター情報:
        名前: {character_name}
        種類: {character_type}
        トピック: {story_topic}
        """

    # 生成されたテキストから情報を抽出
    def _extract_information(self, generated_text):
        lines = generated_text.split('\n')
        
        return {
            'personalities': self._extract_personalities(lines),
            'environments': self._extract_environments(lines),
            'initial_state': self._extract_initial_state(lines),
            'abilities': self._extract_abilities(lines)
        }

    # 性格の抽出
    def _extract_personalities(self, lines):
        personalities = []
        personality_mode = False
        for line in lines:
            if '性格：' in line:
                personality_mode = True
                continue
            elif '特技や能力：' in line:
                personality_mode = False
            elif personality_mode and line.strip().startswith('-'):
                personalities.append(line.strip()[2:].strip())
        return personalities

    # 環境の抽出
    def _extract_environments(self, lines):
        environments = {}
        env_pattern = re.compile(r'\[ENV(\d+)\](.*)')
        for line in lines:
            match = env_pattern.search(line)
            if match:
                env_num = match.group(1)
                env_desc = match.group(2).strip()
                environments[f'ENV{env_num}'] = env_desc
        return environments

    # 初期状態の抽出
    def _extract_initial_state(self, lines):
        initial_state_mode = False
        for line in lines:
            if '[Initial State]' in line:
                initial_state_mode = True
                continue
            elif initial_state_mode and line.strip():
                return line.strip()
        return ""

    # 特技や能力の抽出
    def _extract_abilities(self, lines):
        abilities = []
        ability_mode = False
        for line in lines:
            if '特技や能力：' in line:
                ability_mode = True
                continue
            elif ability_mode and line.strip().startswith('-'):
                abilities.append(line.strip()[2:].strip())
            elif line.strip() and not line.strip().startswith('-') and ability_mode:
                ability_mode = False
        return abilities