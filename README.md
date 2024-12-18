# LLM_nurturing_game
このプロジェクトは、論文 "Unbounded: A Generative Infinite Game of Character Life Simulation" の対話システムに焦点を当てた実装です。
大規模言語モデル（LLM）を活用して、ユーザーが作成したオリジナルキャラクターと動的で自然な対話を楽しむことができます。

## 機能

- カスタマイズ可能なキャラクター作成
- リアルタイムのキャラクターステータス管理
- 動的な環境システム
- インタラクティブな対話システム
- AIによるストーリー生成

## 必要条件

- Python 3.10以上
- OpenAI API キー
- 以下のPythonパッケージ:
  - openai
  - streamlit
  - os
  - re

## インストール方法

1. リポジトリをクローン:
```bash
git clone [repository-url]
cd LLM_nurturing_game
```

2. 必要なパッケージをインストール:
```bash
pip install -r requirements.txt
```

3. 環境変数の設定:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

## 使用方法

1. アプリケーションの起動:
```bash
cd LLM_nurturing_game/src
streamlit run main.py
```

2. ブラウザで表示されるUIから:
   - キャラクターの名前を入力
   - キャラクターの種類を選択
   - ストーリーのトピックを設定
   - 「ゲームを開始」をクリック

3. ゲーム内での操作:
   - テキスト入力欄にアクションを入力
     - キャラクターとの対話や環境の移動が可能
     - 空腹度が100，エネルギーが0にならないようにアクションを取って下さい
   - 「送信」ボタンでアクションを実行
   - サイドバーでステータスと環境情報を確認
   - 必要に応じて「ゲームをリセット」ボタンで初期状態に戻る

## ゲームシステムの詳細

### キャラクターステータス
- 空腹度 (0%が最適)
- エネルギー (100%が最適)
- 楽しさ (100%が最適)
- 衛生状態 (100%が最適)

### 環境システム
- 5つの異なる環境を生成
- 各環境は詳細な説明付き
- 環境間の移動が可能

### AIシステム
- OpenAI GPT-4を使用した対話生成
- ユーザーアクションの解釈
- 動的なストーリー展開
- キャラクターの反応生成

## クラス構造

### GameState
メインのゲーム状態管理クラス
- キャラクター情報の管理
- ステータスの追跡
- 環境の管理
- 対話履歴の記録
- AIとの対話処理

### 主要メソッド
- `initialize_game()`: ゲームの初期設定
- `usr_simulation()`: ユーザー入力の処理
- `world_simulation()`: ゲーム世界の更新
- 各種ヘルパーメソッド

## 参考文献
以下の論文を基にしています：
```bash
@misc{li2024unboundedgenerativeinfinitegame,
      title={Unbounded: A Generative Infinite Game of Character Life Simulation}, 
      author={Jialu Li and Yuanzhen Li and Neal Wadhwa and Yael Pritch and David E. Jacobs and Michael Rubinstein and Mohit Bansal and Nataniel Ruiz},
      year={2024},
      eprint={2410.18975},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2410.18975}, 
}
```

## 注意事項

- OpenAI APIの利用には有効なAPIキーが必要です
- APIの使用には料金が発生する場合があります
- 大量のAPIリクエストを生成する可能性があるため、使用量に注意してください
