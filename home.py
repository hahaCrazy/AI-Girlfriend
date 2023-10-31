from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from langchain.schema.messages import SystemMessage
from langchain.prompts import MessagesPlaceholder
from langchain.chat_models import ChatOpenAI, AzureChatOpenAI
from langchain.agents.openai_functions_agent.agent_token_buffer_memory import AgentTokenBufferMemory
from langchain.agents import AgentExecutor

from langchain.agents import Tool
from utils import Toolset
from utils import StreamHandler

import os
from dotenv import load_dotenv

import streamlit as st
from streamlit_image_select import image_select
from PIL import Image

from langchain.memory.chat_message_histories import StreamlitChatMessageHistory

import json

from utils_prompt import get_rules, get_scene, get_image_trigger
import random

if "page_index" not in st.session_state:
    st.session_state["page_index"] = 0
if "sophia_index" not in st.session_state:
    st.session_state["sophia_index"] = random.randint(0, 2)

characters = ["mina", "rias_gremory", "sophia", "serena"]

#--------------------
st.set_page_config(page_title=f"Girlfriend Chat", page_icon="👧")
st.title(f'💬Chat With Your Girlfriend')

#图片选择器，切换avatar
gallery_placeholder = st.empty()
with gallery_placeholder.container():
    img_index = image_select(
        label="Please Select Your Girlfriend!",
        images=[
            "./gallery/mina.png",
            "./gallery/rias_gremory.png",
            "./gallery/sophia.png",
            "./gallery/serena.png"
        ],
        captions=[
            "Mina",
            "Rias Gremory",
            "Sophia",
            "Serena"
        ],
        index=st.session_state["page_index"],
        return_value="index",
        use_container_width=False,
        key="avatar"
    )
    #切换图片则重新刷新页面
    if st.session_state["page_index"] != img_index:
        st.session_state["page_index"] = img_index
        #st.rerun()

#加载角色数据---------------------------------------------------
character_name = characters[st.session_state["page_index"]]
data_folder = f"./characters/agent_character/{character_name}/"
with open(f"{data_folder}{character_name}_info.json", "r") as f:
    info = json.load(f)
#角色信息
ai_name = info["character"]["name"]
ai_type = info["character"]["type"]
desc = info["character"]["desc"]
appearance = info["character"]["appearance"]
interests = info["character"]["interests"]
personality = info["character"]["personality"]
occupation = info["character"]["occupation"]
shared_memory = info["character"]["shared_memory"]
#角色图片资源
introduce_img = f"{data_folder}{info['img']['introduce']}"
page_icon = f"{data_folder}{info['img']['page_icon']}"
ai_avatar = f"{data_folder}{info['img']['avatar']}"

#个人信息-----
tip1 = info["character"]["short_desc"]["occupation"]
tip2 = info["character"]["short_desc"]["personality"]
words = get_image_trigger(st.session_state["page_index"])
with st.expander(":green[**ℹ️ Character Information**]", expanded=True):
    col_img, col_txt = st.columns([0.25, 0.75])
    with col_img:
        st.image(introduce_img, width=150)
    with col_txt:
        st.write(f"""
        **◾ Name:**  {ai_name}

        **◾ Cateogry:**  {ai_type}

        **◾ Occupation:** {tip1}

        **◾ Personality:** {tip2}

        **◾ Img trigger words:** {words}
        """)

st.info(f""" **Image Trigger Prompt Ex**: give me your ***selfie***. give me a image that you ***on the bed***. give me a image that you ***on the beach***. give me a ***full-body-shot*** of you. etc ... 
        """, icon="👉")
st.write("-------")


class Bot():
    def __init__(self) -> None:
        #load_dotenv(".env")
        self.msgs = StreamlitChatMessageHistory(key=character_name)

    @st.cache_resource(show_spinner="loading resources...")
    def setup_agent(_self, ai_name, scene_index = -1):
        #获取规则信息
        rule1, rule_str = get_rules(ai_name)

        avatar_str = f"""{desc}
        1. Your name is {ai_name}. {rule1}
        2. {appearance}
        3. {interests}
        4. {personality}
        5. {occupation}
        6. {shared_memory}
        """

        greet = ""
        if scene_index >= 0:
            #获取带有场景对话的内容
            scene_str, greet = get_scene(1, scene_index)
            avatar_str += scene_str
        else:
            greet = f"Hi! I am your girlfriend {ai_name}. You can ask me anything."

        #角色信息拼接
        prompt_str = f"""{avatar_str}
        {rule_str}
        """

        system_message = SystemMessage(
                content=(prompt_str)
        )
        prompt = OpenAIFunctionsAgent.create_prompt(
                system_message=system_message,
                extra_prompt_messages=[MessagesPlaceholder(variable_name="history")]
            )
        llm = ChatOpenAI(temperature = 0, streaming=True, max_tokens=500)
        # llm = AzureChatOpenAI(
        #         temperature=0,
        #         model_name="gpt-35-turbo",
        #         openai_api_base=os.environ.get("AZURE_ENDPOINT"),
        #         openai_api_version=os.environ.get("AZURE_OPENAI_VERSION"),
        #         deployment_name=os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME"),
        #         openai_api_key=os.environ.get("AZURE_OPENAI_KEY"),
        #         openai_api_type="azure",
        #     )

        memory = AgentTokenBufferMemory(memory_key="history", llm=llm)

        file_path = f"{data_folder}{character_name}_img.csv"
        if os.path.exists(file_path) == False:
            raise Exception(f"Error: {file_path} not found")
        toolset = Toolset(file_path)
        tools = [
                Tool(
                    name="Local_Image_Search",
                    func=toolset.get_db_image,
                    description=f"""You are an excellent image retrieval tool. 
                    You have recorded some of {ai_name}'s personal photos, images and pictures.
                    The tool is triggered when being asked for a graphic image such as a photo, drawing, picure, selfie, etc. and the words "show me, send me, send, give me, can I see it" appear in the prompt.
                    Finally it returns and displays a image.""",
                )
            ]
        
        agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt)
            
        agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True,
                                        return_intermediate_steps=True)
        return agent_executor, llm, greet

    def main(self):
        #session_msg = st.expander("View the message contents in session state[streamlit]")
        human_avatar = "./img/human.jpg"

        #获取大模型资源
        scene_index = st.session_state["sophia_index"] if st.session_state["page_index"] == 2 else -1 #对话场景的index
        if st.session_state["page_index"] == 0:
            scene_index = -2
        agent_executor, llm, greet = agent_executor, llm, greet = self.setup_agent(ai_name, scene_index)

        if len(self.msgs.messages) == 0:
            #从数据库加载
            # if st.session_state["page_index"] == 0:
            #     self.msgs.add_user_message("你总是那么叛逆，有时候需要冷静下来。")
            #     self.msgs.add_ai_message("""
            #     冷静？我宁可疯狂！毕竟，我们只有一次生命，不是吗？"我是生活的恶魔，死亡的噩梦！"
            #     """)
            self.msgs.add_ai_message(greet)
        
        agent_executor.memory.chat_memory = self.msgs

        for msg in self.msgs.messages:
            if msg.content:
                if msg.type == "ai":
                    st.chat_message("ai", avatar=ai_avatar).write(msg.content)
                elif msg.type == "human":
                    st.chat_message("human", avatar=human_avatar).write(msg.content)

        if input := st.chat_input(placeholder=f"I'm your girlfriend {ai_name}. Ask me anything!"):
            print("question: " + input)
            st.chat_message("human", avatar=human_avatar).write(input)
            #流式传输
            # with st.chat_message("ai", avatar=ai_avatar):
            #     llm.callbacks = [StreamHandler(st.empty())]
            #     response = agent_executor({"input": input})["output"]
            #     print("answer: *************")
            #     print(response)
            #     print("*************")
            #非流式传输
            response = agent_executor({"input": input})["output"]
            st.chat_message("ai", avatar=ai_avatar).write(response)
            print("answer: *************")
            print(response)
            print("*************")

        # with session_msg:
        #     session_msg.json(self.msgs.messages)

if __name__ == "__main__":    
    bot = Bot()
    bot.main()