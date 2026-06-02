"""
Author: Coder729
Date: 2026/6/3
Description: 
"""
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model  # 1.0 统一入口：根据 model + model_provider 创建聊天模型

load_dotenv(encoding="utf-8")

# ========== 1. init_chat_model实例化模型 ==========
# init_chat_model是1.x版本的主角,会根据给的参数，自动创建 ChatOpenAI 或 ChatAnthropic 等具体的客户端。不需要知道创建了谁，只要用就行。
# 若不写 model_provider="openai"，会报错：原因：qwen-plus 等名称无法自动推断厂商，必须显式指定。
# 对比 0.3：0.3 用 ChatOpenAI 类，类名已表示「OpenAI 兼容」，故无需 model_provider。
# 它最大的意义在于：通过 init_chat_model 统一入口，不再需要为每个模型厂商记一套不同的初始化方式，而是先记住同一套调用骨架，再通过参数切换不同模型和 provider。
# 1.x 的思路是：用 init_chat_model 作为统一入口、通过 model、model_provider、api_key、base_url 等参数描述“我要接谁”、同一套代码骨架更容易迁移、统一与维护
print("========== 1. init_chat_model实例化模型 ==========")
model = init_chat_model(
    model="qwen-plus",  
    model_provider="openai",  
    api_key=os.getenv("aliQwen-api"),  
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

print(model.invoke("你是谁").content)

# ========== 2. 同一个系统里面，可以同时存在多个模型 ==========
print("========== 2. 同一个系统里面，可以同时存在多个模型 ==========")
# 同一个系统里面，可以同时存在多个模型，比如
model2 = init_chat_model(
    model="deepseek-v3",
    model_provider="openai",
    api_key=os.getenv("QWEN_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

print(model2.invoke("你是谁").content)





