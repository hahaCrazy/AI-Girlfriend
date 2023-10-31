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

## 项目结构
---
AI-Girlfriend
|-.streamlit                        #streamlit项目的相关配置文件
|   |-config.toml
|   |-secrets.toml                  #存放密钥，代码中可直接用st.secrets["key"]来调用
|-.venv                             #使用venv创建虚拟环境
|
|- characters/agent_character       #角色资源
|            |-mina
|               |-mina_info.json    #存放角色信息，如名字、外貌、性格、职业等
|               |-mina_img.csv      #存放图片，每一张图片对应相应的提示词                    
|            |-rias_gremory
|            |-serena
|            |-sophia
|- gallery                      #streamlit ui资源
|- home.py                      #程序的入口
|- requirements.txt             #需要安装的库
|- utils_prompt.py              #对chatgpt自定义的规则
|- utils.py                     #需要用到的工具，如langchain的代理工具类的封装、chromadb矢量数据库

## 安装方法
python -m venv .venv
pip install -r requirements.txt

## 启动方法
streamlit run .\home.py

## 补充说明
- 当页面内容发生改变时，streamlit会从上往下重新执行代码
- st.session_state用于缓存数据，页面刷新时会被重置
- @st.cache_resource用来缓存模型资源，将传递参数hash处理后返回对应的结果，保证下一次无需再次执行代码，可参考https://docs.streamlit.io/library/advanced-features/caching

![g1](https://github.com/hahaCrazy/AI-Girlfriend/assets/29449583/ec22a52c-0f61-4857-928e-911d4ab9af03)
![g2](https://github.com/hahaCrazy/AI-Girlfriend/assets/29449583/dd2120cb-8a10-4d69-b216-5b07b4eb8929)
![g3](https://github.com/hahaCrazy/AI-Girlfriend/assets/29449583/91163b10-f8f3-4943-b7a0-04397b98df50)
![g4](https://github.com/hahaCrazy/AI-Girlfriend/assets/29449583/ffafc53b-19cd-4736-9d11-645b410ece80)
![g5](https://github.com/hahaCrazy/AI-Girlfriend/assets/29449583/997d1067-7861-42e4-9c0f-f7f527fc5234)
![g6](https://github.com/hahaCrazy/AI-Girlfriend/assets/29449583/01657ccf-756c-43ff-b0ae-aa153ea799f0)

