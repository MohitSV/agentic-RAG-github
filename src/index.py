from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()
index = 'langchain-test-index-mohit'

def trial():
    vector_store = PineconeVectorStore(index=index, embedding=embeddings)
    print(vector_store)

trial()