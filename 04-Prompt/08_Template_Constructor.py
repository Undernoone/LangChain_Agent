"""
Author: Coder729
Date: 2026/6/4
Description:

"""

import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate

load_dotenv()

# ---------- 1. 用构造函数创建模板 ----------
# template：整段话里用 {变量名} 表示占位符；input_variables：列出所有需要「每次调用时传入」的变量名
template = PromptTemplate(
    template="你是一个专业的{role}工程师，请回答我的问题给出回答，我的问题是：{question}",
    input_variables=["role", "question"],
)
"""
对比from_template:
template = PromptTemplate.from_template(
    "你是一个专业的{role}工程师，请回答我的问题给出回答，我的问题是：{question}"
)
"""
print(template)

# ---------- 2. 用 format 填入占位符，得到一条最终提示词字符串 ----------
prompt = template.format(
    role="python开发", question="冒泡排序怎么写"
)
print(prompt)

# ---------- 3. 将格式化后的字符串发给模型（部分聊天模型支持直接传字符串）----------
model = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    api_key=os.getenv("aliQwen-api"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
print(model.invoke(prompt).content)

# ---------- 4. 同一模板复用：换不同参数得到不同提示词 ----------
template_2 = PromptTemplate(
    template="请评价{product}的优缺点，包括{aspect1}和{aspect2}。",
    input_variables=["product", "aspect1", "aspect2"],
)
template_2_prompt1 = template_2.format(product="智能手机", aspect1="电池续航", aspect2="拍照质量")
print(template_2_prompt1)
template_2_prompt2 = template_2.format(product="笔记本电脑", aspect1="处理速度", aspect2="便携性")
print(template_2_prompt2)




