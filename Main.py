import os
import datetime
import xml.etree.ElementTree as ET
import openai
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.docstore.document import Document
import requests
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain import OpenAI, LLMChain, PromptTemplate
import pathlib
import subprocess
import tempfile
import csv
import datetime
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)


load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("API_KEY")
openai.api_key = os.getenv("API_KEY")
query_list = []
categories = ["adoption", "childcare", "childsupport", "custody", "willmaking"]

def get_source():
    for file_name in os.listdir("db//"):
        if file_name.endswith('.txt'):
            name, ext = os.path.splitext(file_name)
            with open(os.path.join("db//", file_name), 'r', encoding="utf8") as file:
                yield Document(page_content=file.read(), metadata={"source": name})


def compare_chunks(sources): 
    source_chunks = []
    splitter = CharacterTextSplitter(separator=" ", chunk_size=720, chunk_overlap=0)
    for source in sources:
        for chunk in splitter.split_text(source.page_content):
            source_chunks.append(Document(page_content=chunk, metadata=source.metadata))
    return Chroma.from_documents(source_chunks, OpenAIEmbeddings(), persist_directory="vector_db\\")


def generate_prompt():
    prompt_template = """
    Chat History:
    ---------
    {chat_history}
    ---------
    Context:
    ---------
    {context}
    ---------
    Legal Question: 
    ---------
    {question}

    Instructions:
    Use the context provided to answer the legal question, taking into consideration of the chat history if any. If you are not certain about the answer, please indicate that you do not have the necessary information and recommend that the user seek legal advice from one of firm XYZ's lawyers. DO NOT make up any information that you do not possess.

"""
    return prompt_template

#@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(3))
def search_db(query, username):
    search_index = Chroma(persist_directory='vector_db', embedding_function= OpenAIEmbeddings())
    global query_list
    query_list.append(query)
    if len(query_list) > 3:
        query_list.pop(0)
    query_sum = ' '.join(query_list)
    embeddings = OpenAIEmbeddings()
    docs = search_index.similarity_search(query_sum, k=3)
    memory = ConversationBufferMemory(memory_key="chat_history", input_key="question")
    PROMPT = PromptTemplate(
        template = generate_prompt(),
        input_variables=["context", "question", "chat_history"],
    )
    chain = load_qa_chain(
    OpenAI(temperature=0),
    chain_type="stuff",
    prompt=PROMPT,  
    memory=memory,
    )
    query = query
    chain({"input_documents": docs, "question": query}, return_only_outputs=True)
    result = chain.memory.buffer
    query_cat = categorize_issue(query, categories)
    store_userdata(username, query, query_cat)
    return result


def categorize_issue(issue, categories):
    prompt = f"Categorize the issue '{issue}' into one of the following categories, and return me with one category. Categories: {', '.join(categories)}."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        n=1,
        temperature=0.9,
        top_p=1,
        presence_penalty=0.6
    )
    issue_category = response.choices[0].text.strip().lower()
    if issue_category in categories:
        return issue_category
    return None


def store_userdata(username, query, query_cat):
    timestamp = datetime.datetime.now()
    fieldnames = ['Timestamp', 'Username', 'User_Query', 'Query_Category']
    filepath = "userdata.csv"
    if not os.path.exists(filepath):
        with open(filepath, "w") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
    try:
        with open(filepath, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow({'Timestamp':timestamp, 'Username':username, 'User_Query':query, 'Query_Category':query_cat})
    except:
        EOFError("Error writing to file")
