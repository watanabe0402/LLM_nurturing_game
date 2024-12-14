from utils import GPTClient
from utils import DialogueFormatter
from .game_initialize import GameInitializer
from .user_simulation import UserSimulator
from .world_simulation import WorldSimulator


class GameState:
    def __init__(self, character_name, character_type, story_topic):
        # GPT Clientの初期化
        self.gpt_client = GPTClient()
        # キャラクターの基本情報
        self.character_name = character_name
        self.character_type = character_type
        self.story_topic = story_topic
        # キャラクターのパラメータ
        self.hunger = 0
        self.energy = 100
        self.fun = 100
        self.cleanliness = 100
        # キャラクターの生成結果
        self.personalities = []
        self.environments = {}
        self.initial_state = ""
        self.abilities = []
        # ユーザーの入力
        self.user_input = ""
        # 現在の環境
        self.current_environment = "ENV1"
        # 対話履歴
        self.dialogue_history = []

        # ゲームの初期設定
        self.game_initializer = GameInitializer(self.gpt_client)

        # DialogueFormatterの初期化
        self.formatter = DialogueFormatter(character_name=self.character_name, initial_state=self.initial_state)

        # UserSimulatorの初期化
        self.user_simulator = UserSimulator(self.gpt_client)

        # WorldSimulatorの初期化
        self.world_simulator = WorldSimulator(self.gpt_client)


    # 対話履歴に追加するための関数
    def add_to_history(self, entry_type, content, environment = None, status = None):
        entry = {
            'type': entry_type,
            'content': content,
            'environment': environment,
            'status': status,
            'timestamp': len(self.dialogue_history)
        }
        self.dialogue_history.append(entry)


    # ゲームの初期設定の実行
    def initialize_game(self):
        result = self.game_initializer.initialize(
            character_name=self.character_name,
            character_type=self.character_type,
            story_topic=self.story_topic
        )
        
        # 結果を各フィールドに設定
        self.personalities = result['personalities']
        self.environments = result['environments']
        self.initial_state = result['initial_state']
        self.abilities = result['abilities']
        
        # 初期状態を対話履歴に追加
        self.add_to_history(
            entry_type='initial_state',
            content=self.initial_state,
            environment=self.current_environment
        )


    def _format_environments(self):
        return self.formatter.format_environments(self.environments)

    def _format_recent_story(self, limit=1): 
        return self.formatter.format_recent_story(self.dialogue_history, limit)

    def _format_dialogue_history(self, limit=3):
        return self.formatter.format_dialogue_history(self.dialogue_history, limit)


    # User Simulationの結果を対話履歴に追加するための関数
    def add_user_action(self, action_type, action_content):
        self.add_to_history(
            entry_type='user_action',
            content={
                'action_type':action_type,
                'action_content':action_content
            },
            environment=self.current_environment,
            status={
                'hunger': self.hunger,
                'energy': self.energy,
                'fun': self.fun,
                'cleanliness': self.cleanliness
            }
        )


    # User Simulationの実行
    def usr_simulation(self, user_input):
        self.user_input = user_input
        
        # UserSimulatorを使用してシミュレーション実行
        action_type, action_content = self.user_simulator.simulate(
            user_input=user_input,
            environments=self._format_environments(),
            recent_story=self._format_recent_story(),
            character_status={
                'hunger': self.hunger,
                'energy': self.energy,
                'fun': self.fun,
                'cleanliness': self.cleanliness
            },
            dialogue_history=self._format_dialogue_history(),
            current_environment=self.current_environment
        )
        
        # 結果を履歴に追加
        self.add_user_action(action_type, action_content)


    # World Simulationの実行
    def world_simulation(self):
        result = self.world_simulator.simulate(
            character_name=self.character_name,
            character_type=self.character_type,
            personalities=self.personalities,
            abilities=self.abilities,
            environments=self._format_environments(),
            recent_story=self._format_recent_story(),
            current_environment=self.current_environment,
            user_input=self.user_input,
            character_status={
                'hunger': self.hunger,
                'energy': self.energy,
                'fun': self.fun,
                'cleanliness': self.cleanliness
            }
        )
        
        # 状態の更新
        self.hunger = result['status']['hunger']
        self.energy = result['status']['energy']
        self.fun = result['status']['fun']
        self.cleanliness = result['status']['cleanliness']
        
        if result['current_environment']:
            self.current_environment = result['current_environment']
        
        # 履歴への追加
        self.add_to_history(
            entry_type='world_simulation',
            content={
                'story_progress': result['story_progress'],
                'response': result['response'],
                'action_need': result['action_need']
            },
            environment=self.current_environment,
            status=result['status']
        )