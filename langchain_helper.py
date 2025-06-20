from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredURLLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

import time
import os
import shutil
from secret import OPENAI_API_KEY



llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    api_key=OPENAI_API_KEY,
)


def delete_existing_vector_store():
    if os.path.exists("my_local_faiss_index"):
        if os.path.isfile("my_local_faiss_index"):
            os.remove("my_local_faiss_index")
        else:
            shutil.rmtree("my_local_faiss_index")

def create_vector_store(urls,main_progress_bar):

    # load the documents from the URLs
    main_progress_bar.text("Loading Data from given URLs.....")
    loader = UnstructuredURLLoader(urls=urls)
    data = loader.load()

    # split the documents into chunks
    main_progress_bar.text("Splitting Data into smaller chunks.....")
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ".", ","],
        chunk_size=1000,
    )
    docs = text_splitter.split_documents(data)
    time.sleep(1)

    #create embeddings and save it to FAISS index
    main_progress_bar.text("Creating Vector Embedding.....")
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vector_store = FAISS.from_documents(docs, embeddings)

    #save FAISS vector locally
    main_progress_bar.text("Updating vector store with new data....")
    delete_existing_vector_store()
    time.sleep(1)
    vector_store.save_local("my_local_faiss_index")
    main_progress_bar.text("URL processed successfully.")
    time.sleep(1)
    main_progress_bar.empty()


def load_vector_store():
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    return FAISS.load_local("my_local_faiss_index", embeddings, allow_dangerous_deserialization=True)


def get_answer_from_vector_store(query):
    vector_store = load_vector_store()
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})

    
    # Create RetrievalQA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )
    result = qa_chain({"query": query}, return_only_outputs=True)
    print(result)
    return result