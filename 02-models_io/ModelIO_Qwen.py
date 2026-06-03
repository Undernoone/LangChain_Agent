"""
Author: Coder729
Date: 2026/6/3
Description:
"""

import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_community.chat_models.tongyi import ChatTongyi

load_dotenv(encoding="utf-8")

# ========== 1. 初始化通义千问聊天模型 ==========
print("========== 1. 初始化通义千问聊天模型 ==========")
# 这里走的是阿里云原生集成，不是 OpenAI 兼容接口路线，因此不需要手动填写 base_url。
chat_llm = ChatTongyi(
    model="qwen-plus",
    api_key=os.getenv("aliQwen-api"),
    streaming=True,
)

# ========== 2. 调用方式一：invoke 一次性返回 ==========
print("========== 2. 调用方式一：invoke 一次性返回 ==========")
print(chat_llm.invoke("你是谁").content)
print(type(chat_llm.invoke("你是谁")))
# ========== 3. 调用方式二：stream 流式返回 ==========
print("========== 3. 调用方式二：stream 流式返回 ==========")
for chunk in chat_llm.stream([HumanMessage(content="你好，你是谁")], streaming=True):
    print(chunk.content, end="")
print()

# 可以看到ChatTongyi是在langchain_community下的，而ChatDeepSeek是直接在langchain_deepseek下的
# 说明DeepSeek拥有自己独立的包，意味着它会得到更好的维护和更及时的功能更新
# 他们都是LangChain 设计的精髓所在，意味着可以用完全相同的代码结构去调用它们
# 后续的 invoke、stream 等操作方式都是一模一样的。这就是 LangChain 作为框架的核心价值
