import streamlit as st
from pathlib import Path
from langchain.document_loaders import CSVLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI, AzureChatOpenAI
import os

from dotenv import load_dotenv
load_dotenv(".env")

st.title('CSV Question and answer ChatBot')


csv_file_uploaded = st.file_uploader(label="Upload your CSV File here")


if csv_file_uploaded is not None:
    def save_file_to_folder(uploadedFile):
        # Save uploaded file to 'content' folder.
        save_folder = 'content'
        save_path = Path(save_folder, uploadedFile.name)
        with open(save_path, mode='wb') as w:
            w.write(uploadedFile.getvalue())

        if save_path.exists():
            st.success(f'File {uploadedFile.name} is successfully saved!')
            
    save_file_to_folder(csv_file_uploaded)
    
    loader = CSVLoader(file_path=os.path.join('content/', csv_file_uploaded.name))

    # Create an index using the loaded documents
    index_creator = VectorstoreIndexCreator()
    docsearch = index_creator.from_loaders([loader])

    llm = AzureChatOpenAI(
                temperature=0,
                model_name="gpt-35-turbo",
                openai_api_base=os.environ.get("AZURE_ENDPOINT"),
                openai_api_version=os.environ.get("AZURE_OPENAI_VERSION"),
                deployment_name=os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME"),
                openai_api_key=os.environ.get("AZURE_OPENAI_KEY"),
                openai_api_type="azure",
            )

    # Create a question-answering chain using the index
    chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.vectorstore.as_retriever(), input_key="question")

    #Creating the chatbot interface
    st.title("Chat wtih your CSV Data")

        # Storing the chat
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []

    if 'past' not in st.session_state:
        st.session_state['past'] = []


    def generate_response(user_query):
        response = chain({"question": user_query})
        return response['result']
    
    
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            st.chat_message("ai").write(st.session_state["generated"][i])
            st.chat_message("human").write(st.session_state["past"][i])
            # message(st.session_state["generated"][i], key=str(i))
            # message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
    
    if user_input := st.chat_input(placeholder=f"Ask Question From your Document"):
        output = generate_response(user_input)
        print(output)
        # store the output 
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)