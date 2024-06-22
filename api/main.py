from fastapi import FastAPI
from fastapi.responses import JSONResponse
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
import openai
import os
from chatbot.utils import initialize_db, search_translate


app = FastAPI()

model = ChatOpenAI(
        openai_api_key="sk-proj-5kIxbwPbgoyfNNcLJ8MNT3BlbkFJpe7bZRBWmYBJnZtAleTZ",
        model="gpt-4",
        temperature=0)

embeddings = HuggingFaceEmbeddings()

initialize_db(
        embeddings,
        data_directory="./data",
        glob="*.*",
        db_name="./chroma_db",
    )

db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)


@app.post("/")
def chatbot(query: str):
    response = search_translate(query, model, db, "rw", "en")
    return JSONResponse(content={
        "data": {
            "reply": response["generate text"],
        }
    }, status_code=200)
