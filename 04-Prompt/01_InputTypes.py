"""
Author: Coder729
Date: 2026/6/4
Description:
invoke支持多种输入类型：字符串、Message 列表、元组列表、字典列表
"""

import os
import asyncio
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

model = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    api_key=os.getenv("aliQwen-api"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)


def demo_message_objects():
    """推荐：显式 Message 对象，角色与字段最清晰。"""
    messages = [
        SystemMessage(content="你是一个专业的数学助手，回答要简短。"),
        HumanMessage(content="你好，你是谁？"),
    ]
    resp = model.invoke(messages)
    print(type(resp), resp.content[:80] if resp.content else "")


def demo_tuple_list():
    """元组列表：与 ChatPromptTemplate.from_messages 的写法一致。"""
    messages = [
        ("system", "你是一个专业的数学助手，回答要简短。"),
        ("human", "你好，你是谁？"),
    ]
    resp = model.invoke(messages)
    print(type(resp), resp.content[:80] if resp.content else "")


def demo_dict_list():
    """字典列表：与 OpenAI Chat Completions 等 API 的请求体形状接近。"""
    messages = [
        {"role": "system", "content": "你是一个专业的数学助手，回答要简短。"},
        {"role": "user", "content": "你好，你是谁？"},
    ]
    resp = model.invoke(messages)
    print(type(resp), resp.content[:80] if resp.content else "")


async def demo_ainvoke_tuple():
    """异步调用同样支持元组简写。"""
    resp = await model.ainvoke([("user", "用一句话说明什么是素数")])
    print(type(resp), resp.content[:80] if resp.content else "")

if __name__ == "__main__":
    print("--- Message 对象列表 ---")
    demo_message_objects()
    print("--- 元组列表 ---")
    demo_tuple_list()
    print("--- 字典列表 ---")
    demo_dict_list()
    print("--- ainvoke + 元组 ---")
    asyncio.run(demo_ainvoke_tuple())


"""
异步是什么意思？异步是一种不阻塞等待的编程模式——发起一个耗时操作后，不原地等待它完成，
而是继续执行其他代码，等操作完成后通过回调、事件或协程来获取结果。
async声明一个函数是协程	，这个函数可以被挂起和恢复
await声明是一个挂起点
resp = await model.ainvoke([("user", "用一句话说明什么是素数")])的时间线：
时间线：
0ms     → 调用 model.ainvoke()，发起网络请求
0ms     → 遇到 await，函数挂起，让出控制权
0-500ms → 事件循环执行其他任务（如果有）
500ms   → 网络响应返回
500ms   → 事件循环恢复协程，赋值给 resp
500ms+  → 执行 print，打印结果
"""
