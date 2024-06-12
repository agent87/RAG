import hydra
from hydra.core.hydra_config import HydraConfig
from omegaconf import DictConfig
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
import openai
import os

from api.chatbot.utils import initialize_db, search

@hydra.main(config_path="conf", config_name="base", version_base=None)
@hydra.main(config_path="conf", config_name="openai", version_base=None)
def main(cfg: DictConfig):
    # openai.api_key = cfg.openai.api_key
    os.environ["OPENAI_API_KEY"] = cfg.openai.api_key
    
    initialize_db(
        OpenAIEmbeddings(),
        data_directory=cfg.data_directory,
        glob=cfg.glob,
        db_name=cfg.db_name
    )

    model = ChatOpenAI()

    db = Chroma(persist_directory=cfg.db_name, embedding_function=HuggingFaceEmbeddings())

    query = "In the fourth quarter of 2023, GDP at current market prices was estimated at Frw 4,500 billion"
    print(search(query, model, db))

if __name__ == "__main__":
    main()