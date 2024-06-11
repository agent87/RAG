from langchain_community.document_loaders import DirectoryLoader, UnstructuredFileLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma

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

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    split_documents = text_splitter.split_documents(documents)
    
    db = Chroma.from_documents(split_documents, embeddings, persist_directory=db_name)
    return db

def search(query, db):
    results = db.similarity_search_with_score(query)
    result = {
        "query": query,
        "content": results[0][0].page_content,
        "source": results[0][0].metadata["source"],
        "metadata": results[0][0].metadata,
        "score": results[0][1]
    }
    return result