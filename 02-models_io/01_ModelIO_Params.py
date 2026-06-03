"""
Author: Coder729
Date: 2026/6/3
Description:
"""
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
load_dotenv(encoding="utf-8")

# ========== 1. 实例化时设置常用参数 ==========
# temperature：控制输出随机性，0 更确定、高重复，越大越随机、越有创意。
# 通常取 0~2，源于 OpenAI API 约定；具体上下界以所用 API 文档为准。
# 超过 2（如 2.1）可能被部分接口拒绝或截断，且与 2.0 效果差异不大，建议不超过 2。
print("========== 1. 实例化时设置常用参数 ==========")
model = init_chat_model(
    model="deepseek-v4-flash",
    model_provider="openai",
    api_key=os.getenv("deepseek-api"),
    base_url="https://api.deepseek.com",
    temperature=0.7,  # 0～1，越高越随机；此处略高便于看到多次输出差异
    # max_tokens=256,  # 可选：限制单次回复长度
)

# - content：正文
# - response_metadata：厂商原始元数据
# - usage_metadata：统一整理后的 token 用量
print("========== 2. 输出 ==========")
print("输出是：",model.invoke("写一句关于春天的词，14 字以内"))
# <class 'langchain_openai.chat_models.base.ChatOpenAI'>
print("type(model)是:",type(model))
# <class 'str'>
print("type(model.invoke.content)是:",type(model.invoke("写一句关于春天的词，14 字以内").content))
# <class 'langchain_core.messages.ai.AIMessage'>
print("type(model.invoke)是:",type(model.invoke("写一句关于春天的词，14 字以内")))
print("usage_metadata是:",model.invoke("写一句关于春天的词，14 字以内").usage_metadata)

# ========== 3. 多次调用观察参数效果（如 temperature 对多样性的影响） ==========
print("========== 3. 不同temperature输出 ==========")
for i in range(15):
    print(f"--- 第 {i + 1} 次，temperature = {model.temperature:.1f} ---")
    print(model.invoke("你是一位冰淇淋店的店员，请你为我推荐一个冰淇淋口味").content)
    print()
    model.temperature += 0.1

