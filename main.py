import hydra
from hydra.core.hydra_config import HydraConfig
from omegaconf import DictConfig
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

from api.chatbot.utils import initialize_db, search

@hydra.main(config_path="conf", config_name="base", version_base=None)
@hydra.main(config_path="conf", config_name="openai", version_base=None)
def main(cfg: DictConfig):
    initialize_db(
        HuggingFaceEmbeddings(),
        data_directory=cfg.data_directory,
        glob=cfg.glob,
        db_name=cfg.db_name
    )

    db = Chroma(persist_directory=cfg.db_name, embedding_function=HuggingFaceEmbeddings())

    print(search("In the fourth quarter of 2023, GDP at current market prices was estimated at Frw 4,500 billion", db))

if __name__ == "__main__":
    main()