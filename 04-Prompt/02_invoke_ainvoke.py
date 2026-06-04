"""
Author: Coder729
Date: 2026/6/4
Description:
介绍invoke和ainvoke的区别
invoke是同步调用，会阻塞等待，直到模型返回结果
ainvoke是异步调用，不会阻塞等待，遇到 await 时挂起，让事件循环执行其他任务
"""

import os
import asyncio
import time
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, SystemMessage

load_dotenv()

# ---------- 1. 实例化聊天模型（两种方式共用）----------
model = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    api_key=os.getenv("aliQwen-api"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)


# ---------- 2. 同步调用（invoke）----------
def demo_invoke():
    """同步调用：阻塞等待，一次性返回完整结果"""
    print("\n" + "=" * 50)
    print("【同步调用 invoke】")
    print("=" * 50)

    messages = [
        SystemMessage(
            content="你是一个法律助手，只回答法律问题，超出范围的统一回答：非法律问题无可奉告"
        ),
        HumanMessage(content="简单介绍下广告法，一句话告知50字以内"),
    ]

    print(f"开始调用... (时间: {time.strftime('%H:%M:%S')})")
    start_time = time.time()

    # 同步调用：这里会阻塞等待
    response = model.invoke(messages) # 这里就不输出了，我只对比耗时

    end_time = time.time()
    print(f"调用完成... (时间: {time.strftime('%H:%M:%S')})")
    print(f"耗时: {end_time - start_time:.2f}秒")

# ---------- 3. 异步调用（ainvoke）----------
async def demo_ainvoke():
    """异步调用：不阻塞等待，await 时让出控制权"""
    print("\n" + "=" * 50)
    print("【异步调用 ainvoke】")
    print("=" * 50)

    print(f"开始调用... (时间: {time.strftime('%H:%M:%S')})")
    start_time = time.time()

    # 异步调用：遇到 await 会挂起，让事件循环执行其他任务
    response = await model.ainvoke(
        SystemMessage(content="你是一个法律助手，只回答法律问题，超出范围的统一回答：非法律问题无可奉告"),
        HumanMessage(content="简单介绍下广告法，一句话告知50字以内"),
    )

    end_time = time.time()
    print(f"调用完成... (时间: {time.strftime('%H:%M:%S')})")
    print(f"耗时: {end_time - start_time:.2f}秒")


# ---------- 4. 异步并发对比（体现异步优势）----------
async def demo_ainvoke_concurrent():
    """异步并发：同时调用多个请求，总耗时远小于串行"""
    print("\n" + "=" * 50)
    print("【异步并发调用（同时发3个请求）】")
    print("=" * 50)

    questions = [
        "什么是Python？一句话回答",
        "什么是机器学习？一句话回答",
        "什么是深度学习？一句话回答",
    ]

    print(f"开始并发调用3个请求... (时间: {time.strftime('%H:%M:%S')})")
    start_time = time.time()

    # 创建3个异步任务，同时执行
    tasks = [model.ainvoke(q) for q in questions]
    responses = await asyncio.gather(*tasks)

    end_time = time.time()
    print(f"全部完成... (时间: {time.strftime('%H:%M:%S')})")
    print(f"总耗时: {end_time - start_time:.2f}秒")
    print(f"如果同步串行执行，需要约 {end_time - start_time:.2f} × 3 = {(end_time - start_time) * 3:.2f}秒")

    # 打印结果
    for i, resp in enumerate(responses, 1):
        print(f"\n问题{i}: {questions[i-1]}")
        print(f"回答: {resp.content}")


# ---------- 5. 同步串行对比（体现异步优势）----------
def demo_invoke_serial():
    """同步串行：一个一个执行，总耗时是累加的"""
    print("\n" + "=" * 50)
    print("【同步串行调用（一个接一个发3个请求）】")
    print("=" * 50)

    questions = [
        "什么是Python？一句话回答",
        "什么是机器学习？一句话回答",
        "什么是深度学习？一句话回答",
    ]

    print(f"开始串行调用3个请求... (时间: {time.strftime('%H:%M:%S')})")
    start_time = time.time()

    responses = []
    for q in questions:
        resp = model.invoke(q)
        responses.append(resp)

    end_time = time.time()
    print(f"全部完成... (时间: {time.strftime('%H:%M:%S')})")
    print(f"总耗时: {end_time - start_time:.2f}秒")

    # 打印结果
    for i, resp in enumerate(responses, 1):
        print(f"\n问题{i}: {questions[i-1]}")
        print(f"回答: {resp.content}")


# ---------- 6. 主函数：对比执行 ----------
async def main():
    """主函数：依次演示各种调用方式"""

    # 1. 同步调用演示
    demo_invoke()

    # 2. 异步调用演示
    await demo_ainvoke()

    # 3. 对比同步串行 vs 异步并发
    print("\n" + "🔥" * 20)
    print("【性能对比：同步串行 vs 异步并发】")
    print("🔥" * 20)

    demo_invoke_serial()      # 同步串行
    await demo_ainvoke_concurrent()  # 异步并发


if __name__ == "__main__":
    asyncio.run(main())
