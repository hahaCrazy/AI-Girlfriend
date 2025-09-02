# AI-Girlfriend
Based on langchain and streamlit. The project used chatgpt-3.5 model.

**Try It Now**
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-girlfriend.streamlit.app/)


## Function
- Customize your own girlfriend
- Chat context memory
- Chat with images you can customize
- Custom rule settings chatgpt

## Technology stack:
- streamlit + langchain + chatgpt
- Note: Character picture information is stored using Chroma vector, that is, the prompt words and pictures correspond one to one. Call the tool of langchain agent to generate pictures

## Project Structure
<pre>
AI-Girlfriend
|-.streamlit                        #Streamlit project configuration files
|   |-config.toml
|   |-secrets.toml                  #Store secrets. In code, you can directly call st.secrets[“key”] to retrieve them.
|-.venv                             #Create a virtual environment using venv
|
|- characters/agent_character       #Character Resources
|            |-mina
|               |-mina_info.json    #Store character information such as name, appearance, personality, occupation, etc.
|               |-mina_img.csv      #Store images, with each image corresponding to its respective prompt word.                    
|            |-rias_gremory
|            |-serena
|            |-sophia
|- gallery                      #streamlit ui resource
|- home.py                      #Program entry point
|- requirements.txt             #Libraries that need to be installed
|- utils_prompt.py              #Custom Rules for ChatGPT
|- utils.py                     #Required tools, such as LangChain's proxy tool wrapper and Chromadb vector database
</pre>
## Installation Method
python -m venv .venv
pip install -r requirements.txt

## Startup Method
streamlit run .\home.py

## Supplementary Notes
- When page content changes, Streamlit re-executes the code from top to bottom.
- st.session_state is used for caching data and will be reset when the page refreshes.
- @st.cache_resource is used to cache model resources. It processes the passed parameter hash and returns the corresponding result, ensuring the code does not need to be executed again on subsequent requests. For reference, see https://docs.streamlit.io/library/advanced-features/caching.

![g1](https://github.com/hahaCrazy/AI-Girlfriend/assets/29449583/ec22a52c-0f61-4857-928e-911d4ab9af03)
![g2](https://github.com/hahaCrazy/AI-Girlfriend/assets/29449583/dd2120cb-8a10-4d69-b216-5b07b4eb8929)
![g3](https://github.com/hahaCrazy/AI-Girlfriend/assets/29449583/91163b10-f8f3-4943-b7a0-04397b98df50)
![g4](https://github.com/hahaCrazy/AI-Girlfriend/assets/29449583/ffafc53b-19cd-4736-9d11-645b410ece80)
![g5](https://github.com/hahaCrazy/AI-Girlfriend/assets/29449583/997d1067-7861-42e4-9c0f-f7f527fc5234)
![g6](https://github.com/hahaCrazy/AI-Girlfriend/assets/29449583/01657ccf-756c-43ff-b0ae-aa153ea799f0)

