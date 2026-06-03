"""
Author: Coder729
Date: 2026/6/3
Description: langchain0.3需要明确说明我使用的是谁家的包、类
"""
import os
from dotenv import load_dotenv  # 从 .env 文件加载环境变量，避免把 API Key 写进代码
from langchain_openai import ChatOpenAI # OpenAI 兼容的聊天模型封装，可配合 base_url 接国内平台
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv(encoding="utf-8")  # encoding 指定 utf-8，避免 .env 中中文注释乱码

# ========== 1. 初始化模型llm_0_3 ==========
print("========== 1. 初始化模型llm_0_3 ==========")
# langchain0.3需要明确说明我使用的是谁家的包、类
# 比如说这里的ChatOpenAI就是OpenAI家定义好的一个类，https://reference.langchain.com/python/langchain-openai/chat_models/base/ChatOpenAI
# 虽然说是OpenAI家的类，但是可以连接非OpenAI的服务器QWEN，因为QWEN主动“模仿”（兼容）了OpenAI的接口格式
# 什么叫兼容OpenAI？ 兼容OpenAI就是指让习惯OpenAI的开发者能零成本使用阿里模型，不用再学一遍原生协议
# 有没有不兼容的？ 如在ChatOpenAI类中的api_key写错成QWEN的dashscope_api_key就会报错，反之同理
llm_0_3 = ChatOpenAI(
    model="deepseek-v3.2",  # 模型名需与阿里百炼「模型广场」中的调用名一致
    api_key=os.getenv("QWEN_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 阿里百炼 OpenAI 兼容接口地址
)

# ========== 2. 调用大模型结果 ==========
print("========== 2. 调用大模型结果 ==========")
# invoke是什么一句话：把你的输入（比如一个问题）发给大模型，然后拿回输出（模型的回答）。
# invoke最基本用法：输入字符串---"什么是invoke"，返回消息对象AIMessage
# invoke复杂用法：输入列表---SystemMessage(content="你是一个专业的AI老师") , HumanMessage(content="什么是invoke？")
# invoke返回的是什么？ 每个类有自己的返回逻辑，比如ChatOpenAI返回AIMessage、PromptTemplate返回字符串
response_simple = llm_0_3.invoke("你是谁")
response_difficult = llm_0_3.invoke([SystemMessage(content="你是一个专业的AI老师") , HumanMessage(content="什么是invoke？")])

# ========== 3. 打印结果 ==========
print("========== 3. 打印结果 ==========")
# response 为 AIMessage 消息对象，这是定义好的，ChatOpenAI调用invoke就是AIMessage，返回包含 content、additional_kwargs 等元数据
# https://reference.langchain.com/python/langchain-core/messages/ai/AIMessage
print(response_simple)  # 打印完整对象
print(response_difficult)  # 打印完整对象
print(response_difficult.content) # AIMessage 90%的场景最应该关注content
# 计算成本、调试异常、Agent 分别用 token_usage、finish_reason、tool_calls等等等等，很好理解，AIMessage就是存储各种信息的

