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
        openai_api_key=f"{os.getenv('OPENAI_API_KEY')}",
        model="gpt-4",
        temperature=0)

embeddings = HuggingFaceEmbeddings()

initialize_db(
        embeddings,
        data_directory=os.getenv("data_directory"),
        glob=os.getenv("glob"),
        db_name=os.getenv("db_name"),
    )

db = Chroma(persist_directory=f"{os.getenv("db_name")}", embedding_function=embeddings)


@app.post("/")
def chatbot(query: str):
    response = search_translate(query, model, db, "rw", os.getenv("base_language"))
    return JSONResponse(content={
        "data": {
            "reply": response["generate text"],
        }
    }, status_code=200)
