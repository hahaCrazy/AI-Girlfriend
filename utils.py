from langchain.embeddings import OpenAIEmbeddings
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
import platform
os_name = platform.system()
if os_name != "Windows":
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
    import sqlite3


from langchain.vectorstores import Chroma
from langchain.callbacks.base import BaseCallbackHandler

import csv
import json
from langchain.schema import Document

import os
import streamlit as st

from langchain.agents import Tool



def enable_chat_history(func):
    pass


class Toolset:
    def __init__(self, path):
        self.db = self._init_csv_db(path)

    def get_db_image(self, prompt: str) -> str:
        print("\nget_db_image prompt:", prompt)
        response = self.db.similarity_search(prompt, k=1)
        
        for data in response:
            res = json.loads(data.page_content)
            print("->", res[1])

        if response and len(response) > 0:
            res = json.loads(response[0].page_content)
            print("\nget_db_image prompt response: ", res[1])
            return res[1]
        return "Sorry. Not found it."

    def get_sd_image(prompt: str) -> str:
        pass
    
    def get_avatar_info(self):
        pass
    
    def _init_csv_db(_self, file_path):
        doc_list = []
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                doc = Document(page_content=json.dumps(row))
                doc_list.append(doc)

        #embeddings = OpenAIEmbeddings()
        embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        file_name = os.path.basename(file_path)
        name, ext = os.path.splitext(file_name)

        #db = Chroma.from_documents(doc_list, embedding=embeddings, persist_directory="./info_db")
        #db.persist()
        db = Chroma.from_documents(doc_list, embedding=embeddings, collection_name=name)
        #res = db.similarity_search(query="", k=1)
        #print(json.loads(res[0].page_content)[2])
        return db
    
    def _get_csv_db(self, folder_path):
        #embeddings = OpenAIEmbeddings()
        embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

        db = Chroma(persist_directory=folder_path, embedding_function=embeddings)
        return db
        
        
        

class StreamHandler(BaseCallbackHandler):
    
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs):
        self.text += token
        self.container.markdown(self.text)
