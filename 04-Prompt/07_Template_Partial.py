"""
Author: Coder729
Date: 2026/6/4
Description:
PromptTemplate 的 new_partial() 方法
partial顾名思义，是部分的意思
定义好一个模板时，可以用partial方法固定固定不变的变量，得到一个新的新模板
之后直接使用新模板的invoke或format方法，传入变化的变量，得到最终的提示词
"""

from langchain_core.prompts import PromptTemplate

# ---------- 1. 创建带两个占位符的模板 ----------
template = PromptTemplate.from_template(
    "你是一个专业的{role}工程师，请回答我的问题给出回答，我的问题是：{question}"
)

# ---------- 2. new_partial(role="python开发")：固定 role，得到「新模板」----------
# 新模板只剩 {question} 需要填，适合多轮只换问题、不换角色的场景
print(template) # 原始模板可以看到有两个占位符{role和question}
new_partial = template.partial(role="python开发")
print(new_partial) # 新模板只剩 {question} 需要填
print(type(new_partial))

# ---------- 3. 对新模板 format，只传 question 即可 ----------
prompt = new_partial.format(question="冒泡排序怎么写？")
prompt_2 = new_partial.invoke({"question": "冒泡排序怎么写？"})
print(prompt)
print(type(prompt))
print(prompt_2)
print(type(prompt_2))

