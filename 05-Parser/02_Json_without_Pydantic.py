"""
Author: Coder729
Date: 2026/6/14
Description: 
在提示词里直接用自然语言告诉模型“请返回 JSON 格式，包含 q 和 a 两个字段”
然后通过解析器把模型输出的文本转成 Python 字典
注意，这种方式只是“建议”模型输出 JSON，并不能严格保证模型一定会输出合规的 JSON，属于软约束；
真正需要稳定格式时，应配合 get_format_instructions() 或模型自带的 JSON 模式。(03_Json_Pydantic)
"""


import os
from loguru import logger
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

load_dotenv(encoding="utf-8")

# 在系统消息里直接写明：返回 json，且包含 q（问题）、a（答案）字段
chat_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是一个{role}，请简短回答我提出的问题，结果返回json格式，q字段表示问题，a字段表示答案。",
        ),
        ("human", "请回答:{question}"),
    ]
)

prompt = chat_prompt.invoke(
    {"role": "AI助手", "question": "什么是LangChain，简洁回答100字以内"}
)

model = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    api_key=os.getenv("aliQwen-api"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 模型返回的可能是带 JSON 的文本
result = model.invoke(prompt)
print(f"模型原始输出:\n{result}")

# 创建 JSON 解析器（不绑 Pydantic 时，解析结果为 dict/list）
parser = JsonOutputParser()
# 尝试从 result 的 content 中解析出 JSON
result_with_parser = parser.invoke(result)
logger.info(f"解析后的结构化结果:\n{result_with_parser}")
logger.info(f"结果类型: {type(result_with_parser)}")  # <class 'dict'>




