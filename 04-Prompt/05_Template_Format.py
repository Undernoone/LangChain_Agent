"""
Author: Coder729
Date: 2026/6/4
Description:
PromptTemplate 的 format() 方法
format() 方法是 `PromptTemplate` 最常用的方法：填入变量后直接得到一条字符串。
"""


from langchain_core.prompts import PromptTemplate

# ---------- 1. 创建模板（from_template 自动推断 {role}、{question}）----------
template = PromptTemplate.from_template(
    "你是一个专业的{role}工程师，请回答我的问题给出回答，我的问题是：{question}"
)
# PromptTemplate 会自动找出 {role} 和 {question} 两个占位符
print(template)

# ---------- 2. format 填入变量，得到「最终一条提示词字符串」----------
prompt = template.format(role="python开发", question="二分查找算法怎么写？")
print(prompt)
# 类型是 str，可直接传给 model.invoke(prompt)
print(type(prompt))
# 必须传入所有占位符
try:
    prompt = PromptTemplate.from_template(role="python开发")
except Exception as e:
    print("报错：",e)
try:
    prompt = PromptTemplate.from_template(r="python开发", question="二分查找算法怎么写？")
except Exception as e:
    print("报错：",e)
