"""
【案例】模型调用：流式调用（stream / astream）

对应教程章节：第 13 章 - 提示词与消息模板 → 4、调用大模型的调用方式

知识点速览：
- stream：同步流式输出，边生成边返回，适合打字机效果
- astream：异步流式输出，适合 Web 服务中的流式响应
- 流式的最大价值：不是更快算完，而是更快展示，减少用户等待焦虑
- 适用场景：聊天界面、长文本生成、报告生成、代码生成等
"""

import os
import asyncio
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, SystemMessage

load_dotenv()

# ---------- 1. 实例化模型 ----------
model = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    api_key=os.getenv("aliQwen-api"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)


# ========== 第一部分：同步流式调用 stream ==========

def demo_stream():
    """同步流式调用：边生成边输出，打字机效果"""
    print("\n" + "=" * 60)
    print("【同步流式调用 stream】")
    print("=" * 60)

    messages = [
        SystemMessage(content="你叫小问，是一个乐于助人的AI助手"),
        HumanMessage(content="介绍一下你自己，50字以内"),
    ]

    print("模型回答：", end="", flush=True)

    # stream 返回生成器，逐块输出
    for chunk in model.stream(messages):
        print(chunk.content, end="", flush=True)

    print("\n")


# ========== 第二部分：异步流式调用 astream ==========

async def demo_astream():
    """异步流式调用：异步版本，适合 Web 服务"""
    print("\n" + "=" * 60)
    print("【异步流式调用 astream】")
    print("=" * 60)

    messages = [
        SystemMessage(content="你叫小问，是一个乐于助人的AI助手"),
        HumanMessage(content="介绍一下你自己，50字以内"),
    ]

    print("模型回答：", end="", flush=True)

    # astream 返回异步生成器，必须用 async for
    async for chunk in model.astream(messages):
        print(chunk.content, end="", flush=True)

    print("\n")


# ========== 第三部分：流式 vs 非流式对比 ==========

def demo_stream_vs_invoke():
    """对比流式和非流式的用户体验差异"""
    print("\n" + "=" * 60)
    print("【流式 vs 非流式 体验对比】")
    print("=" * 60)

    messages = [
        SystemMessage(content="你是一个AI助手"),
        HumanMessage(content="写一段30字左右的自我介绍"),
    ]

    # 非流式：一次性返回
    print("\n--- 非流式调用（invoke）---")
    print("体验：", end="", flush=True)
    response = model.invoke(messages)
    print(response.content)
    print("感受：等待几秒后，内容突然全部出现")

    # 流式：边生成边输出
    print("\n--- 流式调用（stream）---")
    print("体验：", end="", flush=True)
    for chunk in model.stream(messages):
        print(chunk.content, end="", flush=True)
    print("\n感受：内容逐渐出现，用户感知等待时间更短")


# ========== 第四部分：总结 ==========

def demo_summary():
    """总结流式调用的核心要点"""
    print("\n" + "=" * 60)
    print("【核心知识点总结】")
    print("=" * 60)

    summary = """
    ┌─────────────┬──────────────┬─────────────────┬────────────────────────┐
    │   方式      │   同步/异步  │    返回类型      │       适用场景         │
    ├─────────────┼──────────────┼─────────────────┼────────────────────────┤
    │ stream      │   同步       │ 生成器           │ 命令行脚本、本地应用   │
    │ astream     │   异步       │ 异步生成器       │ Web服务、高并发场景    │
    └─────────────┴──────────────┴─────────────────┴────────────────────────┘
    
    流式调用的核心价值：
    1. 边生成边展示，用户不用傻等
    2. 长文本提前回显，减少等待焦虑
    3. 聊天机器人的"打字机效果"就是基于流式
    
    代码区别：
    - stream：for chunk in model.stream(messages)
    - astream：async for chunk in model.astream(messages)
    """
    print(summary)


# ========== 主函数 ==========

async def main():
    """主函数：依次演示所有流式调用"""
    demo_stream()           # 同步流式
    await demo_astream()    # 异步流式
    demo_stream_vs_invoke() # 对比体验
    demo_summary()          # 总结


if __name__ == "__main__":
    asyncio.run(main())

"""
【输出示例】

============================================================
【同步流式调用 stream】
============================================================
模型回答：你好！我是小问，一个乐于助人的AI助手。我擅长解答问题、帮你理清思路...

============================================================
【异步流式调用 astream】
============================================================
模型回答：你好！我是小问，一个乐于助人的AI助手。我擅长解答问题、帮你理清思路...

============================================================
【流式 vs 非流式 体验对比】
============================================================

--- 非流式调用（invoke）---
体验：你好！我是小问...
感受：等待几秒后，内容突然全部出现

--- 流式调用（stream）---
体验：你...好...！...我...是...小...问...
感受：内容逐渐出现，用户感知等待时间更短

============================================================
【核心知识点总结】
============================================================
...
"""