law_chat

概要

law_chat は、法令や判例を検索し、関連する情報を提供するチャットアプリケーションです。RAG (Retrieval-Augmented Generation) を活用し、ユーザーの質問に対して適切な法的情報を提供します。

特徴

ベクトル検索: 高精度な検索機能で関連する法令や判例を取得

WebSocket通信: 非同期でリアルタイムに応答

カスタマイズ可能な検索範囲: ユーザーが判例の年代を選択可能

データソース

本プロジェクトでは、japanese-law-analysis/data_set のデータを使用させていただきました。
本データはCC0ライセンスのもとで提供されており、自由に利用できます。

環境構築

必要条件

Python 3.10+

pip

インストール手順

# 仮想環境の作成（推奨）
python -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate

# 必要パッケージのインストール
pip install -r requirements.txt

使用方法

アプリの起動

flask run

WebSocketを用いたチャット

ユーザーが入力した質問をサーバーに送信

サーバーが検索し、関連する情報を返す

ストリーミング出力により、リアルタイムにレスポンスを表示

ライセンス

本プロジェクトは MITライセンス のもとで提供されます。

