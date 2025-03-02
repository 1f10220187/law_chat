# law_chat

## 概要

law_chat は、判例を検索し、関連する情報を提供するチャットアプリケーションです。RAG (Retrieval-Augmented Generation) を活用し、ユーザーの質問に対して回答を生成します。


## データソース

本プロジェクトでは、[japanese-law-analysis/data_set](https://github.com/japanese-law-analysis/data_set) のデータを使用させていただきました。
本データはCC0ライセンスのもとで提供されており、自由に利用できます。

# 環境構築

pip

インストール手順

## 仮想環境の作成（推奨）
python -m venv venv<br>
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate

## 必要パッケージのインストール
pip install -r requirements.txt

## 使用方法

### 必要な変数の定義
プロジェクト直下(main.pyと同じ階層)に.envファイルを作成して下さい。<br>
そこで、以下の変数を定義してください。<br>

FLASK_APP=wsgi.py <br>
FLASK_ENV=development <br>
SECRET_KEY={任意のシークレットキー} <br>
USER_AGENT=law_chat_app <br>

OPENAI_API_KEY={openAIのapiキー} <br>
LANGCHAIN_API_KEY={langchainのapiキー} <br>
OPENAI_API_BASE={openAIのエンドポイント} <br>

### アプリの起動
flask run

# ライセンス

本プロジェクトは MITライセンス のもとで提供されます。

