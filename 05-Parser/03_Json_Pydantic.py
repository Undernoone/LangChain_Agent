"""
Author: Coder729
Date: 2026/6/14
Description:
这段代码的核心作用，是教会大模型按照我们提前规定好的“数据格式”来回答。首先，
用一个 Pydantic 模型定义好想要的 JSON 结构（比如包含哪几个字段、每个字段是什么类型）。
接着，JsonOutputParser 会根据这个模型自动生成一段非常详细的“格式说明书”，
并把它拼接到发给模型的提示词里。模型看到这份说明书后，就会放弃自由聊天，只输出纯 JSON 格式的文本。
最后，再用同一个解析器把这个 JSON 文本转成 Python 字典，这样程序就能像翻字典一样直接拿取里面的字段值了。
整个过程让大模型从“随意说话”变成了“按要求填表”，输出的数据稳定、可靠、易于程序处理。
"""



import os
from loguru import logger
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field

load_dotenv(encoding="utf-8")

# 作用：声明期望的 JSON 应包含 time、person、event 三个字符串字段，并附带中文说明。
# 为什么用 Pydantic：LangChain 的解析器能读取这个定义，自动生成 Schema 和格式说明。
# Pydantic 是一个 Python 工具，它让你可以定义数据的形状。
class Person(BaseModel):
    """定义一条「新闻」的结构：时间、人物、事件。用于约束模型输出的 JSON 形状。"""
    time: str = Field(description="时间")
    person: str = Field(description="人物")
    event: str = Field(description="事件")

# 绑定 Pydantic 模型：主要驱动 get_format_instructions() 的 schema；invoke 后得到 dict
parser = JsonOutputParser(pydantic_object=Person)

# 获取「格式说明」：描述 Person 各字段，便于拼进提示词让模型按此输出
format_instructions = parser.get_format_instructions()

# 在 human 消息里加入 {format_instructions}，模型会看到「请按如下格式输出 JSON …」
chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个AI助手，你只能输出结构化JSON数据。"),
        ("human", "请生成一个关于{topic}的新闻。{format_instructions}"),
    ]
)

# 填 topic 和 format_instructions，得到消息列表
prompt = chat_prompt.format_messages(
    topic="小米su7跑车", format_instructions=format_instructions
)
print(prompt)

model = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    api_key=os.getenv("aliQwen-api"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

result = model.invoke(prompt)
print(f"模型原始输出:\n{result}")

# 用同一解析器解析，得到符合 Person 结构的数据（dict，或可转成 Person 实例）
result_with_parser = parser.invoke(result)
print(f"解析后的结构化结果:\n{result_with_parser}")
print(f"结果类型: {type(result_with_parser)}")







