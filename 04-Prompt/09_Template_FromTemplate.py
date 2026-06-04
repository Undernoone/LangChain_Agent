"""
Author: Coder729
Date: 2026/6/4
Description:
from_template 创建 PromptTemplate
from_template可以自动识别模板中的占位符变量。
"""


from langchain_core.prompts import PromptTemplate

# # ---------- 1. 用 from_template 创建：自动从字符串里识别 {role}、{question} ----------
# template = PromptTemplate.from_template(
#     "你是一个专业的{role}工程师，请回答我的问题给出回答，我的问题是：{question}"
# )
#
# # ---------- 2. format 填入变量，得到最终一条字符串 ----------
# prompt = template.format(role="python开发", question="快速排序怎么写？")
# print(prompt)
#
# # ---------- 3. 再举一例：{topic}、{type} 两个占位符 ----------
# template_2 = PromptTemplate.from_template("请给我一个关于{topic}的{type}解释。")
# prompt = template_2.format(topic="量子力学", type="详细")
# print(prompt)


prompt_a = PromptTemplate.from_template("请用一句话介绍{topic}，要求通俗易懂\n")
prompt_b = PromptTemplate.from_template("内容不超过{length}个字")
prompt_all = prompt_a + prompt_b
prompt2 = prompt_all.format(topic="LangChain", length=200)
print(prompt2)





