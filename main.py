import hydra
from hydra.core.hydra_config import HydraConfig
from omegaconf import DictConfig
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
import openai
import os

from api.chatbot.utils import initialize_db, search, translate, search_translate

@hydra.main(config_path="conf", config_name="base", version_base=None)
def main(cfg: DictConfig):
    # openai.api_key = cfg.openai.api_key
    os.environ["OPENAI_API_KEY"] = cfg.openai.api_key

    # embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    embeddings = HuggingFaceEmbeddings()
    
    initialize_db(
        embeddings,
        data_directory=cfg.data_directory,
        glob=cfg.glob,
        db_name=cfg.db_name
    )

    model = ChatOpenAI(
        openai_api_key=f"{cfg.openai.api_key}", 
        model="gpt-4",
        temperature=0)

    db = Chroma(persist_directory=cfg.db_name, embedding_function=embeddings)

    # query = "In the fourth quarter of 2023, GDP at current market prices was estimated at Frw 4,500 billion"
    query = "Mu gihembwe cya kane cya 2023, GDP ku giciro cy’isoko ryagereranijwe kuri miliyari 4.500"
    # to_english = translate(query, "rw", cfg.base_language)
    # response = search(to_english, model, db)
    response = search_translate(query, model, db, "rw", cfg.base_language)

    print(response)

    

if __name__ == "__main__":
    main()