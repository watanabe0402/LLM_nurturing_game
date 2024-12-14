import streamlit as st
from game import GameState


def main():
    # セッション状態の初期化
    if 'game_state' not in st.session_state:
        st.session_state.game_state = NameError
        st.session_state.game_started = False
    
    # タイトル
    st.title('キャラクターシミュレーションゲーム')
    st.write('キャラクターを作成して対話を始めよう！')

    # キャラクター作成フォーム
    if not st.session_state.game_started:
        with st.form('character_creation'):
            character_name = st.text_input("キャラクターの名前")
            character_type = st.text_input("キャラクターの種類（例：猫、犬、ロボット）")
            story_topic = st.text_input("ストーリーのトピック（例：日常生活、冒険、学校生活）")
            
            start_button = st.form_submit_button("ゲームを開始")
        
            if start_button and character_name and character_type and story_topic:
                st.session_state.game_state = GameState(character_name, character_type, story_topic)
                st.session_state.game_state.initialize_game()
                st.session_state.game_started = True
                st.rerun()

    # ゲームのメインループ
    if st.session_state.game_started:
        # サイドバーに環境情報とステータスを表示
        with st.sidebar:
            st.subheader("ステータス")
            # プログレスバーと数値を並べて表示
            st.write("空腹度")
            col_a, col_b = st.columns([4, 1])
            with col_a:
                st.progress(st.session_state.game_state.hunger / 100)
            with col_b:
                st.write(f"{st.session_state.game_state.hunger}%")
            
            st.write("エネルギー")
            col_a, col_b = st.columns([4, 1])
            with col_a:
                st.progress(st.session_state.game_state.energy / 100)
            with col_b:
                st.write(f"{st.session_state.game_state.energy}%")
            
            st.write("楽しさ")
            col_a, col_b = st.columns([4, 1])
            with col_a:
                st.progress(st.session_state.game_state.fun / 100)
            with col_b:
                st.write(f"{st.session_state.game_state.fun}%")
            
            st.write("衛生状態")
            col_a, col_b = st.columns([4, 1])
            with col_a:
                st.progress(st.session_state.game_state.cleanliness / 100)
            with col_b:
                st.write(f"{st.session_state.game_state.cleanliness}%")
            
            # 環境情報の表示
            st.subheader("環境情報")
            st.write(f"現在の環境: {st.session_state.game_state.current_environment}")
            st.write("利用可能な環境:")
            for env_id, desc in st.session_state.game_state.environments.items():
                st.write(f"{env_id}: {desc}")

        # キャラクター情報の表示
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("キャラクター情報")
            st.write(f"名前: {st.session_state.game_state.character_name}")
            st.write(f"種類: {st.session_state.game_state.character_type}")
            st.write(f"トピック: {st.session_state.game_state.story_topic}")
        with col2:
            # 性格と特技の表示
            with st.expander("性格:"):
                for personality in st.session_state.game_state.personalities:
                    st.write(f"- {personality}")
            with st.expander("特技:"):
                for ability in st.session_state.game_state.abilities:
                    st.write(f"- {ability}")

        # 対話履歴の表示
        st.subheader("対話履歴")
        history_container = st.container()
        with history_container:
            for entry in st.session_state.game_state.dialogue_history[-10:]:  # 最新の10件を表示
                if entry['type'] == 'user_action':
                    st.write(f"👤 あなた: {entry['content']['action_content']}")
                elif entry['type'] == 'world_simulation':
                    if entry['content']['response']:
                        st.write(f"🎭 {st.session_state.game_state.character_name}: {entry['content']['response']}")
                    if entry['content']['story_progress']:
                        st.write(f"📖 {entry['content']['story_progress']}")
                    if entry['content']['action_need']:
                        st.write(f"⚠️ {entry['content']['action_need']}")

        # text_inputのkeyをsession_stateで管理
        if 'user_input_text' not in st.session_state:
            st.session_state.user_input_text = ""

        # ユーザー入力フィールド
        user_input = st.text_input(
            "あなたの行動を入力してください", 
            key="user_input_field",
            value=st.session_state.user_input_text
        )
        
        if st.button("送信") and user_input:
            with st.spinner("応答を生成中..."):
                # User Simulation の実行
                st.session_state.game_state.usr_simulation(user_input)
                # World Simulation の実行
                st.session_state.game_state.world_simulation()
                # 入力フィールドをクリア
                st.session_state.user_input_text = ""
                st.rerun()

        # リセットボタン
        if st.button("ゲームをリセット"):
            st.session_state.game_state = None
            st.session_state.game_started = False
            st.rerun()





if __name__ == "__main__":
    main()
