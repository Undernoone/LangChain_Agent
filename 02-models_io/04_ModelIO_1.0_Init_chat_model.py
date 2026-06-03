"""
Author: Coder729
Date: 2026/6/3
Description:
"""

import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv(encoding="utf-8")

# ========== 1. 实例化模型（本例中可由 base_url 推断 provider） ==========
print("========== 1. 实例化模型（本例中可由 base_url 推断 provider） ==========")
# 注意：这里能省略 model_provider，是因为本例刻意选择了更容易推断的 DeepSeek 兼容接口场景。
model = init_chat_model(
    model="deepseek-v4-flash",
    api_key=os.getenv("deepseek-api"),
    base_url="https://api.deepseek.com",
)

# ========== 2. 调用并取正文（两种写法均可） ==========
print("========== 2. 调用并取正文（两种写法均可） ==========")
# 写法一：单条用户输入字符串（最简）
# 仅传 str 时，框架会当作一条 user/human 消息，无法在此形式下单独写 system；要 system 请用写法二或消息对象。
print(model.invoke("你是谁？").content)

# 写法二：与 03_ModelIO_0.3_ChatOpenAI.py 相同的多角色消息列表（system + user）
# 统一入口的优势主要体现在“初始化更统一”，返回值仍然是 AIMessage。
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "你是谁？"},
]
response = model.invoke(messages)
print(response.content)
