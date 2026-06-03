"""
Author: Coder729
Date: 2026/6/3
Description:用 LangChain 的 ChatOpenAI 类（0.3 经典写法）调用 OpenAI 兼容接口
"""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv(encoding="utf-8")

# ========== 1. 初始化聊天模型（OpenAI 兼容接口） ==========
print("========== 1. 初始化聊天模型（OpenAI 兼容接口） ==========")
# 这里选择 qwen-plus + 阿里百炼兼容端点，目的是演示“如何把兼容接口接进 LangChain 模型对象”。
chat_llm = ChatOpenAI(
    model="qwen-plus",
    api_key=os.getenv("QWEN_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# ========== 2. 调用模型并打印回复 ==========
print("========== 2. 调用模型并打印回复 ==========")
# 这里直接传入多角色消息列表，后续章会继续系统讲解 Message 体系。
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "你是谁？"},
]

response = chat_llm.invoke(messages)
print(response.content)

#0.3和1.0就是把原生再继续封装一下，1.0 就是把 0.3 再进行一次二开
