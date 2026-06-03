"""
Author: Coder729
Date: 2026/6/3
Description: 
"""

import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
load_dotenv(encoding="utf-8")

# ========== 1. 实例化模型一：通义/百炼（OpenAI 兼容） ==========
print("========== 1. 实例化模型一：通义/百炼（OpenAI 兼容） ==========")
llm_qwen = init_chat_model(
    model="qwen-plus",
    model_provider="openai",  # 阿里百炼为 OpenAI 兼容接口
    api_key=os.getenv("QWEN_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

print(llm_qwen.invoke("你是谁").content)

# ========== 2. 实例化模型二：DeepSeek 官方 ==========
print("========== 2. 实例化模型二：DeepSeek ==========")
# 显式写 model_provider="deepseek" 更稳妥。若接其他厂商（如 OpenAI 兼容），则需写 model_provider="openai"。
llm_deepseek = init_chat_model(
    model="deepseek-v4-flash",  # 复杂推理或高质量生成可改用 deepseek-v4-pro
    model_provider="deepseek",  # 这里走的是 DeepSeek 官方 provider，而不是阿里百炼兼容端点
    api_key=os.getenv("deepseek-api"),  # .env 中配置 DeepSeek API Key
    base_url="https://api.deepseek.com",
)

print(llm_deepseek.invoke("你是谁").content)






