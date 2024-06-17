# from langchain_text_splitters import CharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import DirectoryLoader, UnstructuredFileLoader
from langchain_openai import ChatOpenAI

import os
import shutil
import requests
import json
import string

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

def initialize_db(
        embeddings,
        data_directory,
        glob="*.pdf",
        db_name="./chroma_db"
):
    loader = DirectoryLoader(
        data_directory,
        glob=glob,
        loader_cls=UnstructuredFileLoader,
        use_multithreading=True,
        silent_errors=True
    )

    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300, 
        chunk_overlap=100,
        length_function=len,
        add_start_index=True)
    split_documents = text_splitter.split_documents(documents)
    
    if(os.path.exists(db_name)):
        shutil.rmtree(db_name)

    db = Chroma.from_documents(split_documents, embeddings, persist_directory=db_name)
    return db

def search(query, model, db, threshold=0.7):
    results = db.similarity_search_with_score(query)

    # if len(results) == 0 or results[0][1] < threshold:
    #     return {
    #         "code": 404,
    #         "message": "Failed to retrieve relevant information.",
    #         "query": query,
    #         "score": results[0][1]       
    #     }
    
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query)

    generated_text = model.predict(prompt)
    
    return generated_text, results

class GoogleTranslate:
    api_url = 'https://translate.googleapis.com/translate_a/single'
    client = '?client=gtx'
    dt = '&dt=t'

def translate(
        text, 
        src_lang, 
        tgt_lang):
    sl = f"&sl={src_lang}"
    tl = f"&tl={tgt_lang}"
    
    # Remove punctuation marks from the input text
    translator = str.maketrans('', '', string.punctuation)
    r = requests.get(f"{GoogleTranslate.api_url}{GoogleTranslate.client}{GoogleTranslate.dt}{sl}{tl}&q={text}")
    if r.status_code == 200:
        response_data = json.loads(r.text)
        translated_text = response_data[0][0][0]
    else:
        translated_text = ""
    return translated_text

def search_translate(query, model, db, src_lang, tgt_lang, threshold=0.7):
    to_english = translate(query, src_lang, tgt_lang)
    generated_text, results = search(to_english, model, db, threshold)
    generated_text_to_src = translate(generated_text, tgt_lang, src_lang)
    content_to_src = translate(results[0][0].page_content, tgt_lang, src_lang)
    result = {
        "query": query,
        "generate text": generated_text_to_src,
        "content": content_to_src,
        "source": results[0][0].metadata["source"],
        "metadata": results[0][0].metadata,
        "score": results[0][1]
    }
    return result
