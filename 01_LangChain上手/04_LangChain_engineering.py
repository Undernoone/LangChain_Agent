"""
Author: Coder729
Date: 2026/6/3
Description:
"工程化" 的方式写 LangChain 代码
配置与代码分离	    API Key 放 .env	            不把密钥提交到 Git，安全
函数封装	        init_llm_client()	        多处复用，不用重复写
日志系统	        logging 替代 print	        区分级别（INFO/ERROR），方便排查
异常分类处理	    分别捕获 ValueError/LangChainException	知道问题出在哪（配置错还是网络错）
脚本入口保护	    if __name__ == "__main__"	被 import 时不会自动运行
"""

import os
import logging
from dotenv import load_dotenv
from langchain_openai import  ChatOpenAI
from langchain_core.exceptions import LangChainException

load_dotenv(encoding="utf-8")

# ----- 日志配置 -----
# logging 是 Python 自带的日志库，不用 pip 安装。用 logger.info() / logger.error() 代替 print，方便区分「普通信息」和「错误」，且可统一格式、写文件等。
# 通过环境变量 LOG_LEVEL 控制输出多少：开发时用 INFO（看得到调试信息），生产时在 .env 里设 LOG_LEVEL=WARNING，就只打警告和错误，减少刷屏。

_log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, _log_level, logging.INFO),
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)  # 当前模块的 logger，后面用 logger.info(...) 即可


# ========== 1. LLM 客户端初始化（封装为函数，便于多处复用） ==========
# 「LLM」= 大语言模型（如通义千问、DeepSeek）。这里把「创建可对话的客户端」封装成一个函数，
#  以后在别处也能直接调 init_llm_client()，不用重复写一长串配置。
def init_llm_client() -> ChatOpenAI:
    print("========== 1. LLM 客户端初始化（封装为函数，便于多处复用） ==========")
    """
    初始化 LLM 客户端（封装成函数，提高复用性）。

    Returns:
        ChatOpenAI: 初始化好的「对话客户端」，可以对其调用 .invoke(问题) 或 .stream(问题)。
    """
    api_key = os.getenv("QWEN_API_KEY")
    if not api_key:
        raise ValueError("环境变量 QWEN_API_KEY 未配置，请检查 .env 文件")

    # 创建客户端：指定用哪个模型、密钥、接口地址，以及「回复风格」相关参数。
    llm = ChatOpenAI(
        model="deepseek-v3.2",  # 模型名称（这里演示的是“DeepSeek 模型 + 阿里百炼兼容接口”）
        api_key=api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 阿里云提供的兼容 OpenAI 的地址
        temperature=0.7,  # 控制「随机程度」：0 更确定、重复性高；1 更随机、更有创意。一般 0.5～0.8 即可。
        max_tokens=2048,  # 单次回复最多生成多少个 token（约等于字数），防止回复过长或超限。
    )
    return llm

# ========== 2. 主逻辑：invoke（一次性） + stream（流式）两种调用方式 ==========

def main():
    try:
        llm = init_llm_client()
        logger.info("LLM客户端初始化成功")

        # ----- 方式一：invoke（一次性拿完整回复） -----
        print("========== 2. 主逻辑：invoke（一次性） + stream（流式）两种调用方式 ==========")
        question = "你是谁"
        response = llm.invoke(question)
        print(f"问题：{question}")
        print(f"回答：{response.content}")

        # ----- 方式二：stream（流式，边生成边输出） -----
        # 模型边想边返回，每次返回一小段（chunk），适合长文或需要「实时看到输出」的场景。
        print("以下是stream流式输出")
        response_stream = llm.stream("介绍下 langchain，300字以内")
        for chunk in response_stream:
            print(chunk.content, end="")  # end="" 表示不换行，紧挨着打

    except ValueError as e:
        logger.error(f"配置错误：{str(e)}")
    except LangChainException as e:
        logger.error(f"模型调用失败：{str(e)}")
    except Exception as e:
        logger.error(f"未知错误：{str(e)}")

if __name__ == "__main__":
    main()

"""
以下为基础知识：
========== 1. 封装的好处 ==========
我在04_LangChain_engineering.py定义一个函数：
def init_llm_client():
    return ChatOpenAI(model="...", api_key="...", base_url="...")
之后就可以
llm1 = init_llm_client()
llm2 = init_llm_client()
如果不封装则需要这样写：
llm1 = ChatOpenAI(model="...", api_key="...", base_url="...")
llm2 = ChatOpenAI(model="...", api_key="...", base_url="...")
非常长且墨迹，而且封装后还可以在别的py文件调用
比如说我在这个文件04_LangChain_engineering.py定义了init_llm_client，
我就可以在另一个文件比如说05_demo.py(不存在，举例用）中
添加 from 04_LangChain_engineering import init_llm_client
这样 05_demo.py也可以直接llm1 = init_llm_client()
这就是模块化的核心： 把通用功能抽出来，多个文件共享。

========== 2. try...except解释 ==========
没有 try...except 时，程序一旦出错就直接崩溃：
没有 try...except 时候如下：
num = int("abc")  
print("如果我没输出说明程序崩溃了")
有 try...except 时候如下：
try:
    num = int("abc")  # 这里会出错
    print("如果我没输出说明程序崩溃了")
except ValueError as e:
    print(f"转换失败：{e}")  # 输出：转换失败：invalid literal for int()...
    
========== 3. if __name__ == "main"解释 ==========
如基础知识1封装距离所说，如果不写这个判断直接写main(),则会在05_demo.py直接执行04中的main，
但是我只是想调用init_llm_client
"""
