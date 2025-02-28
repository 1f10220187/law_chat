from law_chat import app
from flask import render_template
from dotenv import load_dotenv

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
def load_vectorstore(url, is_pdf=False):
    vectorstore = Chroma(persist_directory=vectorstore_dir, embedding_function=embeddings)
    print("既存のベクトルストアを読み込みました。")
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

@app.route('/')
def index():
    
    return render_template(
        'index.html'
    )