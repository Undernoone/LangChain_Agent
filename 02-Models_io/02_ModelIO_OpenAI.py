"""
Author: Coder729
Date: 2026/6/3
Description:不用 LangChain，直接用厂商原生的 OpenAI SDK 调用大模型
"""

import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv(encoding="utf-8")

# ========== 1. 初始化客户端（底层 API，直接请求厂商接口） ==========
print("========== 1. 初始化客户端（底层 API，直接请求厂商接口） ==========")
client = OpenAI(
    api_key=os.getenv("deepseek-api"),  # 从环境变量读取，此处以 DeepSeek 为例
    base_url="https://api.deepseek.com",  # 可改为其他 OpenAI 兼容地址（如阿里百炼）
)
# 可以看出区别ChatOpenAI和init_chat_model就已经指定模型名了，但是OpenAI是在后面实例调用时指定的


# ========== 2. 发起对话并打印回复 ==========
print("========== 2. 发起对话并打印回复 ==========")
response = client.chat.completions.create(
    model="deepseek-v4-flash",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello，你是谁？"},
    ],
    stream=False,
)
print("原生回复：",response)
print("原生回复格式：",type(response))
# OpenAI SDK 的返回值需要按原生结构逐层取值：
# result_with_parser -> choices[0] -> message -> content
print(response.choices)
print(response.choices[0].message.content)
# 可以看出输出str嵌套的非常深，体现出了LangChain的方便

'''
对比一下两种方法调用同一个模型的代码量
========== 1. OpenAI==========
client = OpenAI(
    api_key=os.getenv("deepseek-api"),
    base_url="https://api.deepseek.com",
)

result_with_parser = client.chat.completions.create(
    model="deepseek-v4-flash",
    messages=[{"role": "user", "content": "你是谁"}],
)
print(result_with_parser.choices[0].message.content)  # 

========== 2. LangChain==========
llm = ChatOpenAI(
    model="deepseek-v4-flash",
    api_key=os.getenv("deepseek-api"),
    base_url="https://api.deepseek.com",
)

result_with_parser = llm.invoke("你是谁")
print(result_with_parser.content)
'''
