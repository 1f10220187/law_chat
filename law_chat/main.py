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
def format_docs(docs_list):
    return "\n\n".join(doc.page_content for doc in docs_list)

# rag_chain設定関数
def create_rag_chain(vectorstore):
    retriever = vectorstore.as_retriever()
    prompt = hub.pull("rlm/rag-prompt")
    return (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
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

