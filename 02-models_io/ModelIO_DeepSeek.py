"""
Author: Coder729
Date: 2026/6/3
Description:
"""

import os
from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek

load_dotenv(encoding="utf-8")

# ========== 1. 初始化 DeepSeek 聊天模型 ==========
print("========== 1. 初始化 DeepSeek 聊天模型 ==========")
model = ChatDeepSeek(
    model="deepseek-v4-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=os.getenv("deepseek-api"),
)

# ========== 2. 调用并打印回复 ==========
print("========== 2. 调用并打印回复 ==========")
# 返回结果仍然是 LangChain 风格的 AIMessage，因此先读 .content 即可。
print(model.invoke("什么是 LangChain？100 字以内回答，简洁。").content)
