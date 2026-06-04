"""
Author: Coder729
Date: 2026/6/4
Description:
PromptTemplate 的 invoke() 方法
invoke返回的是一个PromptValue对象
这个对象可以使用to_string()方法转换为字符串
也可以使用to_messages()方法转换为消息列表，消息列表中的每个元素都是一个HumanMessage对象，表示一个消息
"""


from langchain_core.prompts import PromptTemplate

# ---------- 1. 创建模板 ----------
template = PromptTemplate.from_template(
    "你是一个专业的{role}工程师，请回答我的问题给出回答，我的问题是：{question}"
)

# ---------- 2. 用 invoke 传入变量（字典），得到 PromptValue 对象 ----------
prompt = template.invoke({"role": "python开发", "question": "冒泡排序怎么写？"})
print(prompt)
print(type(prompt))

# ---------- 3. 从 PromptValue 取内容：to_string() 得到整段字符串 ----------
print(prompt.to_string())
print(type(prompt.to_string()))
print()

# ---------- 4. to_messages()：转成「消息列表」，可接入需要多角色消息的链 ----------
print(prompt.to_messages())
print(type(prompt.to_messages()))

# 为什么不用能直接返回字符串的format而用返回PromptValue的invoke
# 因为要学的LangChain的链式调用 | 要求每一步都返回相同的接口类型。PromptValue就是这个统一接口。
# 而且这个转换方便一点，如果使用format则需要使用StringPromptValue
