from law_chat import app, socketio
from flask import render_template
from flask_socketio import emit
from dotenv import load_dotenv
import time

import os
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import requests
import io
from langchain.schema import Document
from urllib.parse import urlparse
import shutil
from langchain.prompts import PromptTemplate

# .envを読み込む
load_dotenv()

# 環境変数を取得
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")


# Create your views here.
##############RAGで使う変数など#########################
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY 
os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY
llm = ChatOpenAI(model="gpt-4o-mini", openai_api_base=OPENAI_API_BASE)
embeddings = OpenAIEmbeddings(openai_api_base=OPENAI_API_BASE)
vectorstore_dir = "vectorstore"

###########関数################################

# ベクトルストアをロードする関数
def load_vectorstore():
    vectorstore = Chroma(persist_directory=vectorstore_dir, embedding_function=embeddings)
    print("ベクトルストアを読み込みました。")
    return vectorstore

#チェーンを構築用関数
def format_docs(docs):
    if not docs:
        return "※この回答は参考判例を参照していません。\n"
    return "\n\n".join([
        f"【事件名】: {doc.metadata.get('case_name', '不明')}\n"
        f"【裁判所】: {doc.metadata.get('court_name', '不明')}\n"
        f"【判決結果】: {doc.metadata.get('result', '不明')}\n"
        f"【要旨】: {doc.metadata.get('gist', 'なし')}\n"
        f"【判決理由】: {doc.metadata.get('case_gist', 'なし')}\n"
        f"【関連法規】: {doc.metadata.get('ref_law', 'なし')}\n"
        f"------------------------"
        for doc in docs
    ])


# rag_chain設定関数
def create_rag_chain(vectorstore):
    retriever = vectorstore.as_retriever(
        search_type='mmr', # 多様性のある検索
        search_kwargs={
            "k":5,
        }
    )
    prompt_template = PromptTemplate.from_template("""
            あなたは法律に詳しくやさしいAIです。ユーザーの質問に対して、以下の判例を参考にしてわかりやすく回答してください。
            
            判例情報:
            {context}

            ユーザーの質問:
            {question}
            """)
    return (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt_template
        | llm
        | StrOutputParser()
    )

vectorstore = load_vectorstore() # ベクトルストアをロード

#websocketサーバー
@socketio.on("chat_message")
def handle_message(data):
    message = data["message"]
    history = data["history"]  # 過去のやり取り

    # 履歴を使ってプロンプト作成
    context = "\n".join([f"{h['role']}: {h['text']}" for h in history])
    full_prompt = f"{context}\nUser: {message}\nGPT:"

    #OpenAI APIにリクエスト
    
    rag_chain = create_rag_chain(vectorstore) # RAGチェーンを作成
    response_id = str(time.time())  # ユニークなIDを作成
    emit("response_start", {"id": response_id})

    gpt_response = ""

    for chunk in rag_chain.stream(full_prompt):
        # クライアントにリアルタイム送信
        gpt_response += chunk
        emit("response_chunk", {"id": response_id, "text": chunk})
    
    emit("response_end", {"id": response_id})  # メッセージの終了



@app.route('/')
def index():
    return render_template('index.html')

