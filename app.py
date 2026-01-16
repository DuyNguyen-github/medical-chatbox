from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import Pinecone
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
#from langchain.llms import CTransformers
from langchain_ollama import OllamaLLM
from dotenv import load_dotenv
from src.prompt import *
import os


app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY=os.environ.get('PINECONE_API_KEY')

embeddings = download_hugging_face_embeddings()

index_name = "medicalchatbot"

# Embed each chunk and upsert the embeddings into your Pinecone index.
docsearch = Pinecone.from_existing_index(
    index_name=index_name,
    embedding=embeddings,
)

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})

llm = OllamaLLM(
    model="llama2",
    temperature=0.4,
)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

rag_chain = (
    {
        "context": retriever,
        "input": RunnablePassthrough(),
    }
    | prompt
    | llm
)


@app.route("/")
def index():
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    response = rag_chain.invoke(msg)
    print("Response : ", response)
    return response



if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 8080, debug= True)

