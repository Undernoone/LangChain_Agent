"""
Author: Coder729
Date: 2026/6/14
Description: 
"""
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from loguru import logger

load_dotenv(encoding="utf-8")

chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个{role}，请简短回答我提出的问题"),
        ("human", "请回答:{question}"),
    ]
)

prompt = chat_prompt.invoke({"role": "AI助手", "question": "什么是LangChain，简洁回答100字以内"})

model = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    api_key=os.getenv("aliQwen-api"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 调用模型：传入 prompt，得到的是 AIMessage 等对象（原始输出）
result = model.invoke(prompt)
print("原始输出：",result)

# 创建字符串解析器：只做「从 result 里取 content 转成 str」
# 单条 AIMessage 时确实等价于 result.content；用解析器的好处：可链式组合（prompt | model | parser）、
# 流式时统一处理 chunk、多条消息时按约定取最后一条等，且与 JsonOutputParser 等接口一致便于替换。
parser = StrOutputParser()

# 解析：parser.invoke(result) 等价于从 result 中取 content，得到纯字符串
result_with_parser = parser.invoke(result)
print(f"解析后的结构化结果:\n{result_with_parser}")
print(f"结果类型: {type(result_with_parser)}")
