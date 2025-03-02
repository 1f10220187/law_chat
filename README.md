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

使用方法

アプリの起動

flask run

WebSocketを用いたチャット

ユーザーが入力した質問をサーバーに送信

サーバーが検索し、関連する情報を返す

ストリーミング出力により、リアルタイムにレスポンスを表示

# ライセンス

本プロジェクトは MITライセンス のもとで提供されます。

