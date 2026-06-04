"""
【案例】模型调用：批处理（batch / abatch）

对应教程章节：第 13 章 - 提示词与消息模板 → 4、调用大模型的调用方式

知识点速览：
- batch：同步批量调用，一次提交多条输入，统一获得多条结果
- abatch：异步批量调用，适合高并发批量任务
- 适用场景：离线任务、批量摘要、批量分类、批量评估 Prompt 效果
- 核心价值：一次提交，批量返回，大幅提升吞吐量
"""

import os
import asyncio
import time
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

# ---------- 1. 实例化模型 ----------
model = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    api_key=os.getenv("aliQwen-api"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)


# ========== 第一部分：同步批量调用 batch ==========

def demo_batch():
    """同步批量调用：一次处理多个问题"""
    print("\n" + "=" * 60)
    print("【同步批量调用 batch】")
    print("=" * 60)

    questions = [
        "什么是Redis？一句话回答，50字以内",
        "Python的生成器是做什么的？一句话回答，50字以内",
        "Docker和K8s的关系？一句话回答，50字以内",
    ]

    print(f"开始批量处理 {len(questions)} 个问题...")
    start_time = time.time()

    # batch 返回与输入顺序对应的结果列表
    responses = model.batch(questions)

    end_time = time.time()
    print(f"批量完成，总耗时: {end_time - start_time:.2f}秒")
    print(f"平均每个问题: {(end_time - start_time) / len(questions):.2f}秒\n")

    # 打印结果
    for i, (q, r) in enumerate(zip(questions, responses), 1):
        print(f"问题{i}: {q}")
        print(f"回答: {r.content}\n")


# ========== 第二部分：异步批量调用 abatch ==========

async def demo_abatch():
    """异步批量调用：异步版本，适合高并发场景"""
    print("\n" + "=" * 60)
    print("【异步批量调用 abatch】")
    print("=" * 60)

    questions = [
        "什么是Redis？一句话回答，50字以内",
        "Python的生成器是做什么的？一句话回答，50字以内",
        "Docker和K8s的关系？一句话回答，50字以内",
    ]

    print(f"开始异步批量处理 {len(questions)} 个问题...")
    start_time = time.time()

    # abatch 需要 await，返回结果列表
    responses = await model.abatch(questions)

    end_time = time.time()
    print(f"批量完成，总耗时: {end_time - start_time:.2f}秒\n")

    # 打印结果
    for i, (q, r) in enumerate(zip(questions, responses), 1):
        print(f"问题{i}: {q}")
        print(f"回答: {r.content}\n")


# ========== 第三部分：批量 vs 串行性能对比 ==========

def demo_batch_vs_serial():
    """对比批量处理和串行处理的性能差异"""
    print("\n" + "=" * 60)
    print("【批量 vs 串行 性能对比】")
    print("=" * 60)

    questions = [
        "什么是Python？一句话",
        "什么是Java？一句话",
        "什么是Go？一句话",
    ]

    # 串行处理：一个一个来
    print("\n--- 串行处理（循环调用 invoke）---")
    start = time.time()
    serial_responses = []
    for q in questions:
        serial_responses.append(model.invoke(q))
    serial_time = time.time() - start
    print(f"串行耗时: {serial_time:.2f}秒")

    # 批量处理：一次提交
    print("\n--- 批量处理（batch）---")
    start = time.time()
    batch_responses = model.batch(questions)
    batch_time = time.time() - start
    print(f"批量耗时: {batch_time:.2f}秒")

    print(f"\n性能提升: 批量比串行快 {(serial_time - batch_time) / serial_time * 100:.1f}%")
    print("原因：batch 内部对请求进行了并行优化，而串行是一个接一个等待")


# ========== 第四部分：进阶用法——批量处理带 SystemMessage 的请求 ==========

def demo_batch_with_system():
    """批量处理带系统提示的请求"""
    print("\n" + "=" * 60)
    print("【进阶：批量处理带 SystemMessage 的请求】")
    print("=" * 60)

    # 每个请求可以有自己的 system 和 user 消息
    message_lists = [
        [
            SystemMessage(content="你是一个数学专家，回答要简洁"),
            HumanMessage(content="1+1=?"),
        ],
        [
            SystemMessage(content="你是一个历史学家，回答要有趣"),
            HumanMessage(content="长城是什么时候建的？一句话"),
        ],
        [
            SystemMessage(content="你是一个科技评论员，回答要专业"),
            HumanMessage(content="什么是AI？一句话"),
        ],
    ]

    print("开始批量处理不同角色的请求...")
    start_time = time.time()

    # batch 也支持传入消息列表的列表
    responses = model.batch(message_lists)

    end_time = time.time()
    print(f"批量完成，总耗时: {end_time - start_time:.2f}秒\n")

    for i, r in enumerate(responses, 1):
        print(f"请求{i}的回答: {r.content}")


# ========== 第五部分：总结 ==========

def demo_summary():
    """总结批处理的核心要点"""
    print("\n" + "=" * 60)
    print("【核心知识点总结】")
    print("=" * 60)

    summary = """
    ┌─────────────┬──────────────┬─────────────────┬────────────────────────┐
    │   方式      │   同步/异步  │    返回类型      │       适用场景         │
    ├─────────────┼──────────────┼─────────────────┼────────────────────────┤
    │ batch       │   同步       │ List[AIMessage]  │ 离线任务、批量处理     │
    │ abatch      │   异步       │ List[AIMessage]  │ 高并发批量处理         │
    └─────────────┴──────────────┴─────────────────┴────────────────────────┘
    
    批处理的核心价值：
    1. 一次提交多条输入，批量返回结果
    2. 内部并行优化，比串行循环快很多
    3. 适合批量摘要、批量分类、批量评估等离线任务
    
    输入格式：
    - 简单字符串列表：["问题1", "问题2"]
    - 消息列表的列表：[[msg1, msg2], [msg3, msg4]]
    
    代码区别：
    - batch：responses = model.batch(questions)
    - abatch：responses = await model.abatch(questions)
    """
    print(summary)


# ========== 主函数 ==========

async def main():
    """主函数：依次演示所有批处理调用"""
    demo_batch()                # 同步批量
    await demo_abatch()         # 异步批量
    demo_batch_vs_serial()      # 性能对比
    demo_batch_with_system()    # 进阶用法
    demo_summary()              # 总结


if __name__ == "__main__":
    asyncio.run(main())

"""
【输出示例】

============================================================
【同步批量调用 batch】
============================================================
开始批量处理 3 个问题...
批量完成，总耗时: 1.89秒
平均每个问题: 0.63秒

问题1: 什么是Redis？一句话回答，50字以内
回答: Redis是一个开源的内存数据库...

============================================================
【批量 vs 串行 性能对比】
============================================================

--- 串行处理（循环调用 invoke）---
串行耗时: 3.56秒

--- 批量处理（batch）---
批量耗时: 1.89秒

性能提升: 批量比串行快 46.9%

============================================================
【核心知识点总结】
============================================================
...
"""