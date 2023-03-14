import os
import datetime
import xml.etree.ElementTree as ET
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
from xml.dom import minidom
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)


load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("API_KEY")
query_list = []

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
    return Chroma.from_documents(source_chunks, OpenAIEmbeddings())


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
def search_db(query):
    search_index = compare_chunks(get_source())
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

    return result



# def main(username):
#     print(f"Hi {username}, welcome to XYZ Law Firm's Advice Bot! Please ask me anything and I will try my best to answer you! \n However, please note that the reply I provide is not legal advice. If you require legal advice, please book an appointment with one of our helpful lawyers here! (dummyLink). \n Type 'exit' to exit the program. \n")
#     user_input = input(f"{username}: ")
#     while user_input != "exit":
#         result = search_db(user_input).split("AI:")
#         print(result[1])
#         write_to_xml(username, user_input)
#         user_input = input(f"{username}: ")
#     print("Thank you for using our service! Have a nice day!")
    

# def write_to_xml(username, user_input):
#     filepath = "userdata.xml"

#     if not os.path.exists(filepath):
#         root = ET.Element("userdata")
#         tree = ET.ElementTree(root)
#         tree.write(filepath, encoding="utf-8", xml_declaration=True)

#     try:
#         tree = ET.parse(filepath)
#         root = tree.getroot()
#     except ET.ParseError:
#         os.remove(filepath)
#         root = ET.Element("userdata")
#         tree = ET.ElementTree(root)
#         tree.write(filepath, encoding="utf-8", xml_declaration=True)

#     user_element = root.find(f".//{username}")
#     if user_element is None:
#         user_element = ET.SubElement(root, username)

#     new_entry = ET.Element("entry")
#     new_entry.text = user_input
#     user_element.append(new_entry)

#     # Use minidom to generate a well-structured XML file
#     xml_string = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ", newl="\n", encoding="utf-8")
#     with open(filepath, "wb") as f:
#         f.write(xml_string)



# main('bob')